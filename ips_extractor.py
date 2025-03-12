from datetime import datetime, timezone
from darktrace_api import *
import argparse
import socket


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


def main():

    args = parseArgs()
    print(args)

    TAG_ID = args.t or 0

    if args.l:
        list_tags(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN)
        exit(0)

    if args.list_all:
        list_tags(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, all=True)
        exit(0)

    tagname = get_tag_name_from_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, TAG_ID)
    print("Tag name: ", tagname)

    OUTPUT_FILE = args.o if args.o else (f"{tagname}_ips.txt" if tagname else "output_ips.txt")

    entities = get_entities_from_tag_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, TAG_ID)
    written = 0
    with open(OUTPUT_FILE, "w") as f:
        for entity in entities:
            entity_id = entity['entityValue']
            entity_info = get_ip_from_entity_id(DARKTRACE_URL, DARKTRACE_PUBLIC_TOKEN, DARKTRACE_PRIVATE_TOKEN, entity_id)
            print(entity_info)
            entity_ip = entity_info.get("ip") or None
            if entity_ip:
                written += 1 
                f.write(entity_ip + "\n")
   
    print(written, " / ", len(entities), " IPs written to ", OUTPUT_FILE)

def parseArgs():
    ap = argparse.ArgumentParser(description='Darktrace assistant', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=50))
    ap.add_argument('-t', metavar='tagID', help='tag ID')
    ap.add_argument('-o', metavar='outputFile', help='Output file')
    ap.add_argument('-l',  action='store_true', help='List tags info for most used tags')
    ap.add_argument('--list-all', action='store_true', help='List all tags info')

    args = ap.parse_args()
    return args

if __name__ == "__main__":
    main()

"""
arguments
-t TAG_NAME
-l TAG_LIST
-o OUTPUT_FILE
-v -> VERBOSE
-h -> HELP

"""
