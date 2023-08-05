from activecampaign_api.api.abstract_request import AbstractRequest
from activecampaign_api.api.consts import API_ENDPOINT


class WebhookEvents(object):
    def __init__(self, api_request):
        self.api_request = api_request
        self.endpoint = API_ENDPOINT.WEBHOOK_EVENTS

    def get(self):
        return self.api_request.get_request(endpoint=self.endpoint)
