import traceback
import json
import requests.utils
from requests.exceptions import RequestException


class ApiRequest(object):
    def __init__(self, logger, configuration, user_agent):
        self._logger = logger
        self._configuration = configuration
        self._user_agent = user_agent

    def post_request(self, endpoint, params=None):
        return self._request('POST', endpoint, params)

    def get_request(self, endpoint, params=None):
        return self._request('GET', endpoint, params)

    def put_request(self, endpoint, params=None, json_data=None):
        return self._request('PUT', endpoint, params, json_data)

    def delete_request(self, endpoint, params=None):
        return self._request('DELETE', endpoint, params)

    def _request(self, method, endpoint, params, json_data=None):
        try:
            headers = requests.utils.default_headers()
            headers.update({
                'Api-Token': self._configuration.api_token,
                'User-Agent': self._user_agent
            })
            response = requests.request(
                method, self._configuration.api_url + '/' + endpoint,
                params=params, headers=headers, json=json_data)
            response.raise_for_status()
            return json.loads(response.text)
        except RequestException as e:
            self._logger.error(
                "failed to %s request to url=%s, with params=%s. error is: %s" %
                (method, self._configuration.api_url, params, traceback.format_exc()))
            raise e
        except Exception as ex:
            self._logger.error(
                "unexpected Exception while trying to post request. error is: %s"
                % (traceback.format_exc()))
            raise ex
