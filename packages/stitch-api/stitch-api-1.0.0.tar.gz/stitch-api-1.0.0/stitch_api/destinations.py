'''API client for the Destinations end point'''

from stitch_api.api_client import APIClient

class Destinations(APIClient):
    DEFAULT_URI = 'destinations'

    def __init__(self, token):
        super(Destinations,self).__init__(token=token)

    def fetch_destinations(self):
        return self.get(Destinations.DEFAULT_URI, {})
    
    def create_destination(self, params):
        return self.post('{}'.format(Destinations.DEFAULT_URI),params)
    
    def update_destination(self, dest_id, params):
        return self.put('{}/{}'.format(Destinations.DEFAULT_URI,dest_id),params)
    
    def delete_destination(self, dest_id):
        return self.delete('{}/{}'.format(Destinations.DEFAULT_URI,dest_id))