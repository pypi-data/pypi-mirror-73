from collections import defaultdict
from logging import getLogger
from typing import Callable, Iterable, Tuple, Dict, Any

from aiodataloader import DataLoader
from aiohttp.abc import Request

logger = getLogger(__name__)


class BaseDataLoader(DataLoader):
    def __init__(self,
                 endpoint: Callable,
                 request: Request,
                 batch: bool = False,
                 max_batch_size: int = 50,
                 key: str = 'id',
                 proxy_headers: bool = True,
                 **kwargs):
        super().__init__(batch=batch, max_batch_size=max_batch_size, **kwargs)

        self.request = request
        self.endpoint = endpoint
        self.key = key
        self.proxy_headers = proxy_headers

    def __call__(self, **kwargs):
        if self.batch and kwargs.get(self.key):
            keys = self.kwargs_to_keys(kwargs[self.key])
            return self.load_many(keys)
        return self.non_batch_load_fn(**kwargs)

    def prime_results(self, result):
        if not isinstance(result, Iterable):
            result = [result]

        for item in result:
            if isinstance(item, dict) and item.get(self.key):
                self.prime((self.key, item.get(self.key)), item)

    def kwargs_to_keys(self, key) -> Tuple[Tuple[str, Any]]:
        if not isinstance(key, Iterable):
            key = [key]
        return tuple((self.key, val) for val in key)

    @staticmethod
    def keys_to_kwargs(keys) -> Dict[str, Any]:
        d = defaultdict(list)
        for k, v in keys:
            d[k].append(v)
        return dict(d)

    async def non_batch_load_fn(self, **kwargs):
        if self.proxy_headers:
            kwargs['headers'] = self.request.headers

        result = await self.endpoint(**kwargs)
        try:
            self.prime_results(result)
        finally:
            return result

    async def batch_load_fn(self, keys):
        kwargs = self.keys_to_kwargs(keys)
        if self.proxy_headers:
            kwargs['headers'] = self.request.headers

        result = await self.endpoint(**kwargs)
        if not isinstance(result, list):
            result = [result]

        dct = {}
        for key in keys:
            for item in result:
                if key in item.items():
                    dct[key] = item

        return [dct.get(key) for key in keys]
