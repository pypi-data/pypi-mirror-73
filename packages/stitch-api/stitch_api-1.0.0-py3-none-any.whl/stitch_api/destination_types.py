'''API client for the Destination Types end point'''

from stitch_api.api_client import APIClient

class DestinationTypes(APIClient):
    DEFAULT_URI = 'destination-types'

    def __init__(self, token):
        super(DestinationTypes,self).__init__(token=token)

    def fetch_destination_types(self):
        return self.get(DestinationTypes.DEFAULT_URI, {})
    
    def fetch_destination_type_details(self, destination_type):
        return self.get('{}/{}'.format(DestinationTypes.DEFAULT_URI, destination_type),{})
     