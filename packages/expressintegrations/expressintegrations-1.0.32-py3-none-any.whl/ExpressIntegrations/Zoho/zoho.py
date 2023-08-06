from ..HTTP.Requests import *

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
AUTH_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
BASE_URL = 'https://www.zohoapis.com'
AUTH_URL = 'https://accounts.zoho.com'


class zoho:
  import json
  from . import invoices
  from . import contacts
  from . import customerpayments
  from . import users
  from . import items

  def __init__(self, client_id, client_secret, refresh_token):
    self.refresh_token = refresh_token
    post_url = f"{AUTH_URL}/oauth/v2/token"
    auth_body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    result = post(post_url, AUTH_HEADERS, auth_body)
    auth_result = result['content']
    HEADERS['Authorization'] = f"Bearer {auth_result['access_token']}"

  # Contains utilities for interacting with the Zoho API
  def get_org_details(self):
    post_url = f"{BASE_URL}/crm/v2/org"
    return get(post_url, HEADERS)

  def revoke_token(self):
    post_url = f"{AUTH_URL}/oauth/v2/token/revoke?token={self.refresh_token}"
    return post(post_url, AUTH_HEADERS)
