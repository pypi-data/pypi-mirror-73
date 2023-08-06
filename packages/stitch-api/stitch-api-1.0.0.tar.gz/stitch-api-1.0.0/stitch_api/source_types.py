'''API client for the Source Types end point'''

from stitch_api.api_client import APIClient

class SourceTypes(APIClient):
    DEFAULT_URI = 'source-types'

    def __init__(self, token):
        super(SourceTypes,self).__init__(token=token)

    def fetch_source_types(self):
        return self.get(SourceTypes.DEFAULT_URI, {})
    
    def fetch_source_type_details(self, source_type):
        return self.get('{}/{}'.format(SourceTypes.DEFAULT_URI, source_type),{})
     