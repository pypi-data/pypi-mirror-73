import logging
import re
from typing import Mapping, Union, List, Any, Optional, Iterable
from urllib.parse import urljoin

from aiohttp import ClientSession

from gql_ext.exceptions import BadRequestError

logger = logging.getLogger()


class RequestOptions:
    def __init__(self, method: Optional[str], url: str, *,
                 query_params: Union[Mapping, None] = None,
                 json_body: Union[Mapping, None] = None,
                 headers: Union[Mapping, None] = None):
        self.method = method or 'GET'
        self.url = url
        self.params = query_params
        self.json = json_body
        self.headers = headers

    def get_options(self) -> Mapping:
        return {'method': self.method, 'url': self.url, 'json': self.json, 'params': self.params,
                'headers': self.headers}


class BaseHttpRequestMethod:
    BODY_METHODS = ('POST', 'PATCH', 'PUT')
    NO_BODY_METHODS = ('GET', 'DELETE', 'HEAD')

    def __init__(self, path_template: str,
                 session: ClientSession,
                 base_url: str,
                 method: Optional[str] = None,
                 proxy_headers: Optional[Iterable] = None, *args, **kwargs):
        self.base_url = base_url
        self.path_template = path_template
        self.method = method
        self.path_params = None
        self.session = session
        self.proxy_headers = proxy_headers or []

    def get_request_options(self, **kwargs) -> RequestOptions:
        self.path_params = self.get_path_params(self.path_template, **kwargs)
        path = self.format_path(self.path_template, self.path_params)
        url = urljoin(self.base_url, path)
        headers = self.get_headers(kwargs.pop('headers', None))

        query_params = self.get_query_params(kwargs)
        json_body = self.get_json_body(kwargs)

        return RequestOptions(self.method, url, json_body=json_body, query_params=query_params, headers=headers)

    def get_headers(self, headers) -> Union[dict, None]:
        res = {}
        if not headers:
            return
        for header_name, header_value in headers.items():
            if header_name.lower() in self.proxy_headers:
                res[header_name] = header_value
        return res

    @staticmethod
    def get_path_params(path: str, **kwargs) -> Union[List, None]:
        path_params = list()
        params_name = re.findall(r'{(\w*)}', path)
        for p_name in params_name:
            if p_name not in kwargs.keys():
                raise Exception('You must declare all path params')
            path_value = kwargs.get(p_name)
            if isinstance(path_value, (list, tuple)):
                path_value = path_value[0]
            path_params.append((p_name, path_value))
        return path_params

    @staticmethod
    def format_path(path_template: str, path_params: Union[None, List]) -> str:
        formatted_path = path_template
        for k, v in path_params:
            formatted_path = formatted_path.replace('{%s}' % k, str(v))
        return formatted_path

    def get_json_body(self, params: Union[Mapping, None] = None) -> Union[Mapping, None]:
        if self.method in self.BODY_METHODS:
            return {key: val for key, val in params.items() if key not in self.path_params}

    def get_query_params(self, params: Union[Mapping, None] = None) -> Union[List, None]:
        if self.method not in self.NO_BODY_METHODS:
            return
        _params = list()

        for k, v in params.items():
            if (k, v) not in self.path_params:
                if isinstance(v, bool):
                    self.add_param(_params, k, str(v).lower())
                elif isinstance(v, (tuple, list)):
                    if len(v) == 0:
                        raise BadRequestError(f'length of iterable arg {k} is 0')
                    for val in v:
                        self.add_param(_params, k, val)
                else:
                    self.add_param(_params, k, v)

        return _params

    @staticmethod
    def add_param(params: List, key: Any, value: Any):
        if (key, value) not in params:
            params.append((key, value))
