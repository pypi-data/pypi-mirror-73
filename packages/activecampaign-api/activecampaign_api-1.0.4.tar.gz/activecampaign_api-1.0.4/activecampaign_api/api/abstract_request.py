
class AbstractRequest(object):
    def __init__(self, api_request):
        self.api_request = api_request
        self.endpoint = ''

    def create(self, json_data):
        return self.api_request.post_request(endpoint=self.endpoint, json_data=json_data)

    def get_all(self):
        return self.api_request.get_request(endpoint=self.endpoint)

    def get(self, object_id=False):
        if not object_id:
            return self.get_all()
        return self.api_request.get_request(endpoint=self.endpoint + '/' + str(object_id))

    def update(self, object_id, json_data=None):
        return self.api_request.put_request(endpoint=self.endpoint + '/' + str(object_id), json_data=json_data)

    def delete(self, object_id):
        return self.api_request.delete_request(endpoint=self.endpoint + '/' + str(object_id))
