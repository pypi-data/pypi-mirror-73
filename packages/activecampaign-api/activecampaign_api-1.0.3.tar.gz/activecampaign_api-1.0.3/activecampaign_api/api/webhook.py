from activecampaign_api.api.abstract_request import AbstractRequest
from activecampaign_api.api.consts import API_ENDPOINT


class WebHook(AbstractRequest):
    def __init__(self, api_request):
        super(WebHook, self).__init__(api_request)
        self.endpoint = API_ENDPOINT.WEBHOOK
