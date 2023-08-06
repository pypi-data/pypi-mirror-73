from logging import getLogger
from typing import Callable, Optional

from aiohttp.abc import Request

logger = getLogger(__name__)


class BaseResolver:
    endpoint_name: str
    endpoint: Optional[Callable] = None

    def get_endpoint(self, request: Request) -> Optional[Callable]:
        if self.endpoint is not None:
            return self.endpoint
        if not self.endpoint_name:
            return
        try:
            service, endpoint = self.endpoint_name.split('.')
            if not (service and endpoint):
                raise ValueError
        except ValueError as e:
            raise RuntimeError(f'error with parse endpoint name {self.endpoint_name}. '
                               f'use service.endpoint format. {e}')

        service = getattr(request.app, service)
        if not service:
            raise RuntimeError(f'Cant get service {service}')

        endpoint = getattr(service, endpoint, None)
        if not endpoint:
            raise RuntimeError(f'Cant get source method or endpoint for {self.endpoint_name}')

        self.endpoint = endpoint
        return endpoint

    async def load(self, parent, args, ctx, info):
        raise NotImplementedError
