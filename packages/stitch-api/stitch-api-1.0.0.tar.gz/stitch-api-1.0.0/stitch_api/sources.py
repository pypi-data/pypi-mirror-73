'''API client for the Sources end point'''

import json
from stitch_api.api_client import APIClient

class Sources(APIClient):
    DEFAULT_URI = 'sources'

    def __init__(self, token):
        super(Sources,self).__init__(token=token)

    def fetch_sources(self):
        return self.get(Sources.DEFAULT_URI, {})
    
    def fetch_source_details(self, source_id):
        return self.get('{}/{}'.format(Sources.DEFAULT_URI, source_id), {})
    
    def fetch_source_tokens(self, source_id):
        return self.get('{}/{}/tokens'.format(Sources.DEFAULT_URI, source_id), {})
    
    def fetch_source_connection_check(self, source_id):
        return self.get('{}/{}/last-connection-check'.format(Sources.DEFAULT_URI, source_id), {})
    
    def create_source(self, params):
        return self.post('{}'.format(Sources.DEFAULT_URI),params)
    
    def create_source_token(self, source_id):
        return self.post('{}/{}/tokens'.format(Sources.DEFAULT_URI, source_id), {})

    def update_source(self, source_id, params):
        return self.put('{}/{}'.format(Sources.DEFAULT_URI,source_id),params)
    
    def pause_source(self, source_id, params):
        return self.put('{}/{}'.format(Sources.DEFAULT_URI,source_id), params)
    
    def unpause_source(self, source_id):
        json_string = '{"paused_at":null}'
        return self.put('{}/{}'.format(Sources.DEFAULT_URI,source_id), json.loads(json_string))
    
    def delete_source(self, source_id):
        return self.delete('{}/{}'.format(Sources.DEFAULT_URI, source_id), {})
    
    def revoke_source_token(self, source_id, token_id):
        return self.delete('{}/{}/tokens/{}'.format(Sources.DEFAULT_URI, source_id, token_id), {})