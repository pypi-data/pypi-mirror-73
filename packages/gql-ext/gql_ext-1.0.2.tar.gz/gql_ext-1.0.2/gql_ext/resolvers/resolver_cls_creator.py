from functools import partial
from typing import Mapping, Optional, List

from gql_ext.dataloaders import BaseDataLoader
from gql_ext.resolvers.base_resolvers import BaseMutationResolver, BaseSubscriptionResolver, BaseQueryResolver
from gql_ext.utils import import_from_module


def parse_arg(arg_value, parent, ctx):
    if not isinstance(arg_value, str):
        return arg_value
    if arg_value.startswith('parent.'):
        return parent.get(arg_value.split('.')[-1])
    if arg_value.startswith('request.'):
        return ctx['request'].get(arg_value.split('.')[-1])
    return arg_value


def parse_args(arg_value, parent, ctx):
    if isinstance(arg_value, (list, tuple)):
        return [parse_arg(arg, parent, ctx) for arg in arg_value if arg is not None]
    return parse_arg(arg_value, parent, ctx)


def init_loader(preset_args, loader):
    async def parsed_args_loader(resolver, parent, args, ctx, info):
        if preset_args is not None:
            for arg_name, arg_val in preset_args.items():
                args[arg_name] = parse_args(arg_val, parent, ctx)
        return await loader(resolver, parent, args, ctx, info)

    return parsed_args_loader


def set_middlewares(middlewares, loader):
    if not middlewares:
        return loader
    if not isinstance(middlewares, list):
        raise RuntimeError('middlewares must be a list')

    for mid in reversed(middlewares):
        mid = import_from_module(mid)
        loader = partial(mid, call_next=loader)

    async def loader_wrapper(resolver, parent, args, ctx, info):
        return await loader(resolver=resolver, parent=parent, args=args, ctx=ctx, info=info)

    return loader_wrapper


def create_resolver(resolver_name: str = None, loader: str = None, endpoint: str = None,
                    batch: bool = False, dataloader: Optional[str] = None, args: Mapping = None,
                    middlewares: Optional[List[str]] = None, **kwargs):
    attrs = {}

    if resolver_name.startswith('Mutation.'):
        base = BaseMutationResolver
    elif resolver_name.startswith('Subscription.'):
        base = BaseSubscriptionResolver
    else:
        base = BaseQueryResolver
        attrs['dataloader_cls'] = import_from_module(dataloader) if dataloader else BaseDataLoader
        attrs['batch'] = batch

    loader = import_from_module(loader) if loader else base.load
    if not resolver_name.startswith('Subscription.'):
        loader = init_loader(args, loader)

    loader = set_middlewares(middlewares, loader)

    attrs['endpoint_name'] = endpoint
    attrs['load'] = loader

    return type(resolver_name, (base,), attrs)
