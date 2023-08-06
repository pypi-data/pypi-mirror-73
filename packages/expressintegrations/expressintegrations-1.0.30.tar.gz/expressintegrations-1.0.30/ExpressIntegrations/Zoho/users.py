from ..HTTP.Requests import *
from .zoho import HEADERS

BASE_URL = 'https://invoice.zoho.com/api/v3'


def get_user(user_id):
  post_url = f"{BASE_URL}/users/{user_id}"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve user. Result: {result}")
  return result


def search_users(filter_by=None, sort_column='email'):
  # sort_column Allowed Values: name, email, user_role and status
  post_url = f"{BASE_URL}/users?sort_column={sort_column}"
  if filter_by is not None:
    post_url = f"{post_url}&filter_by={filter_by}"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve users. Result: {result}")
  return result
