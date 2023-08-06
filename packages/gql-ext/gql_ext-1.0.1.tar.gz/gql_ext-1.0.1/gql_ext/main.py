import os
from functools import partial
from inspect import isclass, isabstract
from logging import getLogger

from aiohttp import web
from aiohttp.abc import Request, Application
from aiohttp.web_response import Response
from tartiflette import Engine, Scalar

from .clients import mount_to_app
from .config import Config
from .graphiql import set_graphiql_handler
from .resolvers import set_resolver
from .utils import load_file, import_from_module, resolve_paths, ScalarDefinition, import_by_full_path
from .view import create_endpoint, options_handler
from .websocket import set_ws_handlers

logger = getLogger(__name__)


class GqlExt:
    config: Config

    def __init__(self, app: Application, path_to_init_file: str, base_path: str):
        self.config = Config()
        self.app = app
        self.base_path = base_path
        self.initial_config = load_file(path_to_init_file)

        self.schemas = self.initial_config.get('schemas') or {}

    def mount_app(self):
        for service_name, description in (self.initial_config.get('services').items() or []):
            spec = load_file(os.path.join(self.base_path, description['spec']))
            client_cls = self.config.get_client(description.get('client'))

            params = self.config.services_params.get(service_name)
            mount_to_app(app=self.app, cls=client_cls, spec=spec, params=params, service_name=service_name)

        for schema_name, schema_description in self.schemas.items():
            self.handle_schema(schema_name, schema_description)

        if self.config.allow_cors:
            self.allow_cors()

    def handle_schema(self, schema_name, schema_description):
        resolvers_description_file_path = os.path.join(self.base_path, schema_description.get('resolvers'))
        resolvers_description = load_file(resolvers_description_file_path)
        self.set_resolvers(resolvers_description, schema_name)

        sdl_paths = [os.path.join(self.base_path, sdl) for sdl in schema_description.get('sdl') or []]
        sdl_paths = resolve_paths(sdl_paths)

        middlewares = [import_from_module(path) for path in schema_description.get('middlewares') or []]

        self.set_types(sdl_paths, schema_name, schema_description)

        self.mount_endpoint(schema_name, sdl_paths, schema_description.get('modules'),
                            url=schema_description.get('url'), middlewares=middlewares)

    def set_types(self, sdl_paths, schema_name, schema_description):
        types_paths = [os.path.join(self.base_path, types) for types in schema_description.get('types') or []]
        types_paths = resolve_paths(types_paths)
        for types_path in types_paths:
            if types_path.endswith('.graphql'):
                sdl_paths.append(types_path)
            if types_path.endswith('.py'):
                self.set_type(types_path, schema_name)

    @staticmethod
    def set_type(types_path, schema_name):
        module = import_by_full_path(types_path)
        for k, v in module.__dict__.items():
            if not isclass(v) or isabstract(v) or v is ScalarDefinition:
                continue
            if issubclass(v, ScalarDefinition):
                Scalar(k, schema_name=schema_name)(v)

    def allow_cors(self):
        async def on_prepare(req: Request, res: Response):
            if req.headers.get('ORIGIN'):
                res.headers['Access-Control-Allow-Origin'] = req.headers.get('ORIGIN')
            res.headers['Access-Control-Allow-Credentials'] = 'true'

        self.app.on_response_prepare.append(on_prepare)

    def set_resolvers(self, resolvers: dict, schema: str):
        for resolver_name, args in resolvers.items():
            set_resolver(resolver_name, schema, args)

    def mount_endpoint(self, schema, sdl, modules, url=None, middlewares=None):
        if middlewares is None:
            middlewares = []
        allow_cors = self.config.allow_cors
        if not url:
            url = f'/graphql/{schema}'

        async def start(app_, engine=None):
            if engine is None:
                engine = Engine()

            await engine.cook(sdl=sdl, schema_name=schema, modules=modules)
            app_.add_routes([web.post(url, create_endpoint(engine, *middlewares))])

            set_ws_handlers(app_, engine, endpoint_url=f'{url}/ws')

            set_graphiql_handler(app_, True, {'endpoint': url}, url, ['POST'], f'{url}/ws')

            if allow_cors:
                handler = partial(options_handler, allowed_headers=list(self.config.allowed_headers))
                app_.add_routes([web.options(url, handler)])

            logger.debug(f'{schema} schema has been initialized')

        self.app.on_startup.append(start)

# todo: cors - refactoring
