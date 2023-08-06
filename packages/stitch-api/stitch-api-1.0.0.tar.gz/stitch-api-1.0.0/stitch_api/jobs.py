'''API client for the Jobs end point'''

from stitch_api.api_client import APIClient

class Jobs(APIClient):
    DEFAULT_URI = 'sources'

    def __init__(self, token):
        super(Jobs,self).__init__(token=token)
    
    def start_job(self, source_id):
        return self.post('{}/{}/sync'.format(Jobs.DEFAULT_URI,source_id),{})
    
    def stop_job(self, source_id):
        return self.delete('{}/{}/sync'.format(Jobs.DEFAULT_URI,source_id),{})