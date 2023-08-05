import json
import logging
from json import JSONDecodeError
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession
from aiohttp import ContentTypeError

from gql_ext.exceptions import BaseApiException
from .base import BaseHttpRequestMethod

logger = logging.getLogger()


class WSRequestMethod(BaseHttpRequestMethod):
    async def __call__(self, **kwargs):
        self.path_params = self.get_path_params(self.path_template, **kwargs)
        path = self.format_path(self.path_template, self.path_params)
        url = urljoin(self.base_url, path)
        async with self.session.ws_connect(url) as ws:
            logger.debug('Connected ws to %s', url)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        yield msg.json()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break


class HttpRequestMethod(BaseHttpRequestMethod):
    async def __call__(self, **kwargs):
        if not self.method:
            raise NotImplementedError('Not known method')
        if not self.session:
            self.session = ClientSession()
        req_opt = self.get_request_options(**kwargs)

        logger.debug('\nMake request to %s\nParams:\n\tMethod: %s\n\tBody: %s\n\tQuery Params: %s\n\tHeaders: %s',
                     req_opt.url, req_opt.method, req_opt.json, req_opt.params, req_opt.headers)

        async with self.session.request(**req_opt.get_options()) as resp:
            try:
                json_resp = await resp.json()
                logger.debug('Received data: %s', json_resp)
            except (JSONDecodeError, ValueError, ContentTypeError) as e:
                logger.error('Invalid JSON body: %s\nResp: %s', e, resp)
                raise BaseApiException(message={'error': 'Invalid JSON body', 'status_code': resp.status},
                                       status_code=resp.status)
            if resp.status >= 400:
                raise BaseApiException(message=json.dumps({'response': json_resp, 'status_code': resp.status}),
                                       status_code=resp.status)
            return json_resp
