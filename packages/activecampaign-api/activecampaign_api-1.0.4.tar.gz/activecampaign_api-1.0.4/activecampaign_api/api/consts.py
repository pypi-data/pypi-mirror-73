from ..version import __version__

USER_AGENT = "ActiveCampaign-Python/" + __version__


class API_ENDPOINT(object):
    EMAIL_ACTIVITIES = 'emailActivities'
    MESSAGE = 'messages'
    SEGMENT = 'segments'
    ADDRESSES = 'addresses'
    CONTACT = 'contacts'
    FIELD = 'fields'
    FIELD_VALUE = 'fieldValues'
    ACCOUNTS = 'accounts'
    ACCOUNT_CONTACTS = 'accountContacts'
    ACCOUNT_CUSTOM_FIELD_META = 'accountCustomFieldMeta'
    ACCOUNT_CUSTOM_FIELD_DATA = 'accountCustomFieldData'
    WEBHOOK = 'webhooks'
    WEBHOOK_EVENTS = 'webhook/events'
