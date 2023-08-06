'''API client for the Streams end point'''

from stitch_api.api_client import APIClient

class Streams(APIClient):
    DEFAULT_URI = 'sources'

    def __init__(self, token):
        super(Streams,self).__init__(token=token)
    
    def fetch_streams(self, source_id):
        return self.get('{}/{}/streams'.format(Streams.DEFAULT_URI,source_id),{})
    
    def fetch_schema(self, source_id, stream_id):
        return self.get('{}/{}/streams/{}'.format(Streams.DEFAULT_URI,source_id,stream_id),{})
    
    def update_schema(self, source_id, params):
        return self.put('{}/{}/streams/metadata'.format(Streams.DEFAULT_URI, source_id), params)