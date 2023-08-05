
from activecampaign_api.api.abstract_request import AbstractRequest
from activecampaign_api.api.consts import API_ENDPOINT


class EmailActivitiesRequest(AbstractRequest):
    def __init__(self, api_request):
        super(EmailActivitiesRequest, self).__init__(api_request)
        self.endpoint = API_ENDPOINT.EMAIL_ACTIVITIES

    def get(self, params=None):
        return self.api_request.get_request(endpoint=self.endpoint, params=params)
