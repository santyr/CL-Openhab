import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from enum import Enum

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpMethod(Enum):
    POST = 'POST'
    PUT = 'PUT'

def create_headers(openhab_api_key, is_json=True):
    headers = {
        'Authorization': f'Bearer {openhab_api_key}',
        'Content-Type': 'application/json' if is_json else 'text/plain'
    }
    return headers

def configure_openhab_api():
    """
    Reads configuration from a JSON file and extracts OpenHAB URL and API key.

    Returns:
        tuple: OpenHAB URL and API key.
    """
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("config.json not found.")
        return None, None
    openhab_url = config.get('openhab_url')
    openhab_api_key = config.get('openhab_api_key')
    return openhab_url, openhab_api_key

def make_request(url, headers, data, method=HttpMethod.POST):
    if method == HttpMethod.POST:
        response = requests.post(url, headers=headers, data=data, verify=False)
    elif method == HttpMethod.PUT:
        response = requests.put(url, headers=headers, data=data, verify=False)
    response.raise_for_status()
    return response

def check_and_create_items(openhab_url, openhab_api_key, items):
    headers = create_headers(openhab_api_key)

    for item_name, item_config in items.items():
        item_url = f'{openhab_url}/rest/items/{item_name}'
        response = requests.get(item_url, headers=headers, verify=False)
        if response.status_code == 404:
            item_config_json = json.dumps(item_config)
            response = make_request(item_url, headers, item_config_json, method=HttpMethod.PUT)
            if response.status_code != 201:
                raise Exception(f'Failed to create item {item_name}: {response.text}')

def send_data_to_openhab(openhab_url, openhab_api_key, data):
    headers = create_headers(openhab_api_key, is_json=False)

    for item_name, item_value in data.items():
        item_url = f'{openhab_url}/rest/items/{item_name}/state'
        response = make_request(item_url, headers, str(item_value), method=HttpMethod.PUT)
        if response.status_code != 202:
            raise Exception(f'Failed to update item {item_name}: {response.text}')
