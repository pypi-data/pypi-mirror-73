import logging

from activecampaign_api.api.configuration import Configuration
from activecampaign_api.api.consts import USER_AGENT
from activecampaign_api.api.api_request import ApiRequest
from activecampaign_api.api.message import MessageRequest
from activecampaign_api.api.contact import ContactRequest
from activecampaign_api.api.segment import SegmentRequest
from activecampaign_api.api.custom_field import CustomFieldsRequest
from activecampaign_api.api.custom_field_value import CustomFieldValueRequest
from activecampaign_api.api.email_activities import EmailActivitiesRequest
from activecampaign_api.api.webhook import WebHook
from activecampaign_api.api.webhook_events import WebhookEvents


class Api(object):
    def __init__(self, api_url, api_token):
        self._logger = logging.getLogger('activecampaign_api')
        self._api_request = ApiRequest(self._logger, Configuration(api_url, api_token), USER_AGENT)

    @property
    def message(self):
        return MessageRequest(self._api_request)

    @property
    def contact(self):
        return ContactRequest(self._api_request)

    @property
    def segment(self):
        return SegmentRequest(self._api_request)

    @property
    def custom_field(self):
        return CustomFieldsRequest(self._api_request)

    @property
    def custom_field_value(self):
        return CustomFieldValueRequest(self._api_request)

    @property
    def email_activities(self):
        return EmailActivitiesRequest(self._api_request)

    @property
    def webhook(self):
        return WebHook(self._api_request)

    @property
    def webhook_events(self):
        return WebhookEvents(self._api_request)
