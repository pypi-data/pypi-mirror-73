from gql_ext.dataloaders import BaseDataLoader
from .base import BaseResolver


class BaseQueryResolver(BaseResolver):
    batch: bool = False
    dataloader_cls: BaseDataLoader = BaseDataLoader

    async def load(self, parent, args, ctx, info):
        endpoint = self.get_endpoint(ctx['request'])
        if not endpoint:
            return
        dataloader = self.get_dataloader(ctx['request'], endpoint)
        return await dataloader(**args)

    def get_dataloader(self, request, endpoint) -> BaseDataLoader:
        dataloader = getattr(request, self.endpoint_name, None)
        if dataloader is None:
            dataloader = self.dataloader_cls(endpoint=endpoint, request=request, batch=self.batch)
            setattr(request, self.endpoint_name, dataloader)
        return dataloader
