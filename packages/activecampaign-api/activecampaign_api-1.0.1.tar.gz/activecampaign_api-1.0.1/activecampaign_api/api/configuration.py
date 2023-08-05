class Configuration(object):
    def __init__(self, api_url, api_token):
        self._api_token = api_token
        self._api_url = api_url + '/api/3'

    @property
    def api_url(self):
        return self._api_url

    @property
    def api_token(self):
        return self._api_token
