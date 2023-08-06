from ..HTTP.Requests import *
from .hubspot import BASE_URL
from .hubspot import HEADERS


def get_owner(owner_id):
  post_url = f"{BASE_URL}crm/v3/objects/owners/{owner_id}"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve owner. Result: {result}")
  return result
