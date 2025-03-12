from dotenv import load_dotenv
from hashlib import sha1
import urllib3
import requests
import urllib3
import hmac
import os

load_dotenv()

urllib3.disable_warnings()

# will be in command line
DARKTRACE_PUBLIC_TOKEN=os.getenv("DARKTRACE_PUBLIC_TOKEN")
DARKTRACE_PRIVATE_TOKEN=os.getenv("DARKTRACE_PRIVATE_TOKEN")
DARKTRACE_URL=os.getenv("DARKTRACE_URL")

def sign_request(private_token, api_request, public_token, date):
    return hmac.new(private_token.encode('ASCII'), (api_request+'\n'+public_token+'\n'+date).encode('ASCII'), sha1).hexdigest()