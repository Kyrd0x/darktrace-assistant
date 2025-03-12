from datetime import datetime, timezone
from dotenv import load_dotenv  # type: ignore
from hashlib import sha1
import urllib3
import requests
import socket
import hmac
import os


urllib3.disable_warnings()
load_dotenv()

# will be in command line
DARKTRACE_PUBLIC_TOKEN=os.getenv("DARKTRACE_PUBLIC_TOKEN")
DARKTRACE_PRIVATE_TOKEN=os.getenv("DARKTRACE_PRIVATE_TOKEN")
DARKTRACE_URL=os.getenv("DARKTRACE_URL")

def sign_request(private_token, api_request, public_token, date):
    return hmac.new(private_token.encode('ASCII'), (api_request+'\n'+public_token+'\n'+date).encode('ASCII'), sha1).hexdigest()

def get_all_tags(url, public_token, private_token):
    date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    api_route = "/tags"
    
    url = url + api_route
    
    headers = {
        'DTAPI-Token': public_token,
        'DTAPI-Date': date,
        'DTAPI-Signature': sign_request(private_token,api_route,public_token,date)
    }
    try:
        response = requests.get(url, verify=False, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred during the API call: {str(e)}")

def list_tags(url, public_token, private_token, all=False):
    all_tags = get_all_tags(url, public_token, private_token)
    for tag in all_tags:
        tag["device_count"] = len(get_entities_from_tag_id(url, public_token, private_token, tag['tid']))

    print(f"{'Service': <38} {'ID': >3} {'Devices'}")
    print("-" * 55)

    sorted_data = sorted(all_tags, key=lambda x: x['device_count'], reverse=True)
    for tag in sorted_data:
        if not all and tag['device_count'] > 1:
            print(f"{tag['name']: <38} {tag['tid']: >3} {tag['device_count']}")

def get_ip_from_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return "Cant resolve host"
    
def get_entities_from_tag_id(url, public_token, private_token, tag_id):

    date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    api_route = f"/tags/{tag_id}/entities"
    
    url = url + api_route
    
    headers = {
        'DTAPI-Token': public_token,
        'DTAPI-Date': date,
        'DTAPI-Signature': sign_request(private_token,api_route,public_token,date)
    }
    try:
        response = requests.get(url, verify=False, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred during the API call: {str(e)}")

def get_ip_from_entity_id(url, public_token, private_token, entity_id):

    date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    api_route = f"/devices?did={entity_id}"
    
    url = url + api_route
    
    headers = {
        'DTAPI-Token': public_token,
        'DTAPI-Date': date,
        'DTAPI-Signature': sign_request(private_token,api_route,public_token,date)
    }
    try:
        response = requests.get(url, verify=False, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred during the API call: {str(e)}")
    
def get_tag_name_from_id(url, public_token, private_token, tag_id):
    all_tags = get_all_tags(url, public_token, private_token)
    for tag in all_tags:
        if tag['tagId'] == tag_id:
            return tag['tagName']
    return None