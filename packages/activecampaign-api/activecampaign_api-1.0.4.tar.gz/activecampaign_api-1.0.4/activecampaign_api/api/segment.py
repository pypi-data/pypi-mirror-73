from activecampaign_api.api.consts import API_ENDPOINT

ENDPOINT = API_ENDPOINT.SEGMENT

class Segment(object):
    def __init__(self, name=None, logic=None,
                 hidden=None, seriesid=None,
                 links=None, id=None):
        self._id = id
        self._name = name
        self._logic = logic
        self._hidden = hidden
        self._seriesid = seriesid
        self._links = links or []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def logic(self):
        return self._logic

    @property
    def hidden(self):
        return self._hidden

    @property
    def seriesid(self):
        return self._seriesid

    @property
    def links(self):
        return self._links

    def from_dict(self, data):
        if 'id' in data:
            self._id = data['id']
        if 'name' in data:
            self._name = data['name']
        if 'logic' in data:
            self._logic = data['logic']
        if 'hidden' in data:
            self._hidden = data['hidden']
        if 'seriesid' in data:
            self._seriesid = data['seriesid']
        if 'links' in data:
            self._links = data['links']
        return self

    def to_dict(self):
        data = {
            'id': self._id,
            'name': self._name,
            'logic': self._logic,
            'hidden': self._hidden,
            'seriesid': self._seriesid,
            'links': self._links,
        }
        return data


class Segments(object):
    def __init__(self):
        self._segments = []
        self._meta = None

    def from_dict(self, data):
        if 'meta' in data:
            self._meta = data['meta']
        if 'segments' in data and isinstance(data['segments'], list):
            for segment_data in data['segments']:
                self._segments.append(Segment().from_dict(segment_data))
        return self

    @property
    def meta(self):
        return self._meta

    @property
    def segments(self):
        return self._segments


class SegmentRequest(object):
    def __init__(self, api_request):
        self.api_request = api_request

    def get_all(self):
        return Segments().from_dict(self.api_request.get_request(endpoint=ENDPOINT))

    def get(self, segment_id):
        return Segment.from_dict(self.api_request.get_request(endpoint=ENDPOINT + '/' + segment_id))
