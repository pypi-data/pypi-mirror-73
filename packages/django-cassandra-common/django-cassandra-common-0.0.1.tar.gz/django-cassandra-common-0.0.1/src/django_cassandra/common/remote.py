import json
import urllib

import requests


class RemoteModel:
    def __init__(self, request, url):
        self.request = request
        self.url = url

    def _headers(self, override_headers=None):
        base_headers = {'content-type': 'application/json'}
        override_headers = override_headers or {}
        return {**self.request.headers, **base_headers, **override_headers}

    def _cookies(self, override_cookies=None):
        override_cookies = override_cookies or {}
        return {**self.request.COOKIES, **override_cookies}

    def get(self, entity_id=''):
        return requests.get(f'{self.url}{entity_id}', headers=self._headers(), cookies=self._cookies())

    def create(self, entity_data):
        return requests.post(f'{self.url}', data=json.dumps(entity_data), headers=self._headers(),
                             cookies=self._cookies())

    def update(self, entity_id, entity_data):
        return requests.put(f'{self.url}{entity_id}', data=json.dumps(entity_data), headers=self._headers(),
                            cookies=self._cookies())

    def delete(self, entity_id):
        return requests.delete(f'{self.url}{entity_id}', headers=self._headers(), cookies=self._cookies())

    def filter(self, **params):
        params = f'?{urllib.parse.urlencode(params)}'
        return requests.get(f'{self.url}{params}', headers=self._headers(), cookies=self._cookies())
