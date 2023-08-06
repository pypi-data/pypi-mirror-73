from gql_ext.clients.http import HTTPApi


class Config:
    allowed_headers = []
    allow_cors = True
    default_client = 'http'
    services_params = {}
    _clients = {'http': HTTPApi}

    def get_client(self, name):
        if not name:
            name = self.default_client
        return self._clients.get(name)

    def set_client(self, name, client):
        self._clients[name] = client
