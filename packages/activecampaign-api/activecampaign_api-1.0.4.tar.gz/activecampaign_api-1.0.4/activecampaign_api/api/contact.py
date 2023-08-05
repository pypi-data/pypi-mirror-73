
from activecampaign_api.api.abstract_request import AbstractRequest
from activecampaign_api.api.consts import API_ENDPOINT
from activecampaign_api.api.custom_field import CustomFieldsRequest
from activecampaign_api.api.custom_field_value import CustomFieldValueRequest


class Attribute:
    def __init__(self, model, name):
        self.model = model
        self.name = name


class Contact(object):
    def __init__(self, contact_request, id=None, cdate=None, email=None,
                 phone=None, first_name=None,
                 last_name=None):
        self._contact_request = contact_request
        self._data = {}
        self._id = id
        self._cdate = cdate
        self._email = email
        self._phone = phone
        self._first_name = first_name
        self._last_name = last_name
        self._custom_fields = {}
        self._custom_fields_value = {}
        self._fields = {}

    @property
    def id(self):
        return self._id

    @property
    def cdate(self):
        return self._cdate

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def data(self):
        return self._data

    def from_dict(self, data):
        self.data = data
        if 'id' in data:
            self.id = data['id']
        if 'cdate' in data:
            self.cdate = data['cdate']
        if 'email' in data:
            self.email = data['email']
        if 'phone' in data:
            self.phone = data['phone']
        if 'firstName' in data:
            self.first_name = data['firstName']
        if 'lastName' in data:
            self.last_name = data['lastName']
        return self

    def to_dict(self):
        data = {
            'cdate': self.cdate,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        return data

    def __getattr__(self, name):
        value = self.data.get(name, None)
        if value is None:
            raise AttributeError(name)
        return value

    def _get_field_value(self, name):
        field = self._get_field(name)
        value = None
        if field:
            value = self._custom_fields_value.get(field, None)
            if value is None:
                value = CustomFieldValueRequest(self._contact_request.api_request).get(field)
        return value

    def _get_field(self, name):
        if not self._custom_fields:
            self._get_custom_fields()
        return self._custom_fields.get(name, None)

    def _get_custom_fields(self):
        self._custom_fields = CustomFieldsRequest(self._contact_request.api_request).get_all()['fields']


class ContactRequest(AbstractRequest):
    def __init__(self, api_request):
        super(ContactRequest, self).__init__(api_request)
        self.endpoint = API_ENDPOINT.CONTACT

    def create_or_update(self, params):
        return self.api_request.post_request(
            endpoint=self.endpoint + '/sync',
            params=params)

    def lists(self, params):
        return self.api_request.post_request(
            endpoint=self.endpoint + '/contactLists',
            payload=params)

    def automations(self, message_id):
        return self.api_request.post_request(
            endpoint=self.endpoint + '/' + message_id + '/contactAutomations')

    def get_all_to_object(self, params=None):
        if not params:
            params = {"status": "-1", "orders[email]": "ASC"}
        return self.from_dict_to_objects(
            self.api_request.get_request(
                endpoint=self.endpoint,
                params=params))

    def get_all(self, params=None):
        if not params:
            params = {"status": "-1", "orders[email]": "ASC"}
        return self.api_request.get_request(
            endpoint=self.endpoint,
            params=params)

    def from_dict_to_objects(self, data):
        contacts = []
        if 'meta' in data:
            self.meta_data = data['meta']
        if 'contacts' in data and isinstance(data['contacts'], list):
            for contact_data in data['contacts']:
                contacts.append(Contact(self).from_dict(contact_data))
        return contacts
