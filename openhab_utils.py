import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def configure_openhab_api():
    with open('config.json', 'r') as f:
        config = json.load(f)
    openhab_url = config.get('openhab_url')
    openhab_api_key = config.get('openhab_api_key')
    return openhab_url, openhab_api_key

def make_request(url, headers, data, method='POST'):
    if method == 'POST':
        response = requests.post(url, headers=headers, data=data, verify=False)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=data, verify=False)
    return response

def check_and_create_items(openhab_url, openhab_api_key, items):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openhab_api_key}'
    }

    for item_name, item_config in items.items():
        item_url = f'{openhab_url}/rest/items/{item_name}'
        response = requests.get(item_url, headers=headers, verify=False)
        if response.status_code == 404:
            item_config_json = json.dumps(item_config)
            response = make_request(item_url, headers, item_config_json, method='PUT')
            if response.status_code != 201:
                raise Exception(f'Failed to create item {item_name}: {response.text}')

def send_data_to_openhab(openhab_url, openhab_api_key, data):
    headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'Bearer {openhab_api_key}'
    }

    for item_name, item_value in data.items():
        item_url = f'{openhab_url}/rest/items/{item_name}/state'
        response = make_request(item_url, headers, str(item_value), method='PUT')
        if response.status_code != 202:
            raise Exception(f'Failed to update item {item_name}: {response.text}')

