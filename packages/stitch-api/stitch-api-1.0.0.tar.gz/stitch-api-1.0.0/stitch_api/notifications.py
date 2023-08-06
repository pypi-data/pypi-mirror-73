'''API client for the Notifications end point'''

import json
from stitch_api.api_client import APIClient

class Notifications(APIClient):
    DEFAULT_URI = '/notifications/public/v1/api/'

    def __init__(self, token):
        super(Notifications,self).__init__(version=Notifications.DEFAULT_URI,token=token)
    
    def create_custom_email(self, params):
        return self.post('custom-emails', params)
    
    def disable_custom_email(self, email_id, params):
        return self.put('custom-emails/{}'.format(email_id), params)
    
    def re_enable_custom_email(self, email_id):
        json_string = '{"disabled_at": null}'
        return self.put('custom-emails/{}'.format(email_id), json.loads(json_string))
    
    def fetch_custom_emails(self):
        return self.get('custom-emails', {})
    
    def delete_custom_email(self, email_id):
        return self.delete('custom-emails/{}'.format(email_id), {})
    
    def create_webhook(self, params):
        return self.post('hooks', params)
    
    def disable_webhook(self, webhook_id):
        json_string = '{"enable": false}'
        return self.put('hooks/{}'.format(webhook_id), json.loads(json_string))
    
    def re_enable_webhook(self, webhook_id):
        json_string = '{"enable": true}'
        return self.put('hooks/{}'.format(webhook_id), json.loads(json_string))
    
    def fetch_webhooks(self):
        return self.get('hooks', {})
    
    def delete_webhook(self, webhook_id):
        return self.delete('hooks/{}'.format(webhook_id), {})