import logging
from typing import Mapping, Union, List, Optional

from aiohttp import ClientSession

from .requests import HttpRequestMethod, WSRequestMethod

logger = logging.getLogger()


class HTTPApi:
    def __init__(self, base_url: str, session: ClientSession, proxy_headers: Optional[List] = None):
        self.base_url = base_url
        self.session = session
        self.proxy_headers = [proxy_header.lower() for proxy_header in proxy_headers or []]

    @classmethod
    async def create(cls, spec: Optional[Mapping[str, Union[str, Mapping]]] = None,
                     **kwargs):
        session = ClientSession()
        api = cls(**kwargs, session=session)
        api.set_api_methods(spec)
        return api

    async def stop(self):
        await self.session.close()

    def set_api_methods(self, spec: Mapping[str, Union[str, Mapping]]):
        for k, v in spec.items():
            if v.get('method').lower() == 'ws':
                endpoint_cls = WSRequestMethod
            else:
                endpoint_cls = HttpRequestMethod

            setattr(self, k, endpoint_cls(path_template=v['path'],
                                          method=v.get('method'),
                                          base_url=self.base_url,
                                          session=self.session,
                                          proxy_headers=self.proxy_headers))
