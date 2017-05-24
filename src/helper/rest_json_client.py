
from helper.rest_requests import RestRequests
import requests
from requests import packages


packages.urllib3.disable_warnings()


class RestClientException(Exception):
    pass


class RestClientUnauthorizedException(RestClientException):
    pass


class RestJsonClient(RestRequests):
    def __init__(self, hostname, use_https=True):
        self._hostname = hostname
        self._use_https = use_https
        self._session = requests.Session()

    @property
    def session(self):
        return self._session

    def _build_url(self, uri):
        if self._hostname not in uri:
            if not uri.startswith('/'):
                uri = '/' + uri
            if self._use_https:
                url = 'https://{0}{1}'.format(self._hostname, uri)
            else:
                url = 'http://{0}{1}'.format(self._hostname, uri)
        else:
            url = uri
        return url

    def _valid(self, response):
        if response.status_code in [200, 201, 204]:
            return response
        elif response.status_code in [401]:
            raise RestClientUnauthorizedException(self.__class__.__name__, 'Incorrect login or password')
        else:
            raise RestClientException(self.__class__.__name__,
                                      'Request failed: {0}, {1}'.format(response.status_code, response.text))

    def request_put(self, uri, data):
        response = self._session.put(self._build_url(uri), data, verify=False)
        return self._valid(response).json()

    def request_post(self, uri, data):
        response = self._session.post(self._build_url(uri), json=data, verify=False)
        return self._valid(response).json()

    def request_post_files(self, uri, data, files):
        response = self._session.post(self._build_url(uri), data=data, files=files, verify=False)
        return self._valid(response).json()

    def request_get(self, uri):
        response = self._session.get(self._build_url(uri), verify=False)
        return self._valid(response).json()

    def request_get_files(self, uri):
        response = self._session.get(self._build_url(uri), verify=False)
        return self._valid(response)

    def request_delete(self, uri):
        response = self._session.delete(self._build_url(uri), verify=False)
        return self._valid(response).content
