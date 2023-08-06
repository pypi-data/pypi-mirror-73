import hashlib
import json

from ringcentral import SDK


BASE_URL = 'https://platform.ringcentral.com'


class ringcentral:
  def __init__(self, client_id, client_secret, username, password, extension, server_url=BASE_URL):
    rcsdk = SDK(client_id, client_secret, server_url)
    self.platform = rcsdk.platform()
    self.extension = extension
    self.platform.login(username, extension, password)
    self.account_id = self.get_account_details()['id']

  # Contains utilities for interacting with the MailChimp api
  def get_account_details(self, account_id='~'):
    return self.platform.get(f"/restapi/v1.0/account/{account_id}")

  def send_sms(self, sender_number, recipient_number, text):
    post_body = {
        'from': {
            'phoneNumber': sender_number
        },
        'to': [
            {
                'phoneNumber': recipient_number
            }
        ],
        'text': text
    }
    return self.platform.post(f"/restapi/v1.0/account/{self.account_id}/extension/{self.extension}/sms", post_body)
