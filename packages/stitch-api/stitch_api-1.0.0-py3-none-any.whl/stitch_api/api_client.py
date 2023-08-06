'''Stitch API client base class.'''

import json
import os
import requests

class APIClient(object):
    DEFAULT_SCHEMA = 'https'
    DEFAULT_HOST = 'api.stitchdata.com'
    DEFAULT_VERSION = 'v4/'

    def __init__(self, token, schema=None, host=None, version=None):
        if schema == None:
            schema = APIClient.DEFAULT_SCHEMA
        if host == None:
            host = APIClient.DEFAULT_HOST
        if version == None:
            version = APIClient.DEFAULT_VERSION

        self.base_url = '{}://{}/{}'.format(schema,host,version)
        self.token = token
    
    def get(self, uri, params):
       r =  requests.get('{}/{}'.format(self.base_url,uri), headers=self.__headers__(), params=params)
       response = r.text
       if r.status_code == 200 and r.headers['content-type'].find('application/json') == 0:
            response = r.json()
       return r.status_code, response

    def post(self, uri, params):
        headers = self.__headers__()
        headers['content-type'] = 'application/json'
        r = requests.post('{}/{}'.format(self.base_url, uri), headers=headers, data=json.dumps(params))
        response = r.text
        if r.status_code == 200 and r.headers['content-type'].find('application/json') == 0:
            response = r.json()
        return r.status_code, response

    def put(self, uri, params):
        headers = self.__headers__()
        headers['content-type'] = 'application/json'
        r = requests.put('{}/{}'.format(self.base_url, uri), headers=headers, data=json.dumps(params))
        response = r.text
        if r.status_code == 200 and r.headers['content-type'].find('application/json') == 0:
            response = r.json()
        return r.status_code, response

    def delete(self, uri):
        r = requests.delete('{}/{}'.format(self.base_url, uri), headers=self.__headers__())
        response = r.text
        if r.status_code == 200 and r.headers['content-type'].find('application/json') == 0:
            response = r.json()
        return r.status_code, response

    def __headers__(self):
        headers = {
            'Content-Type': 'application/json',
        }
        if self.token != None:
            headers['Authorization'] = 'Bearer {}'.format(self.token)
        return headers