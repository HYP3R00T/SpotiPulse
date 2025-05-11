import json
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import base64

from requests import post

load_dotenv()

# Constants
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


print(SPOTIFY_CLIENT_ID)
print(SPOTIFY_CLIENT_SECRET)

def get_token():
    url = "https://accounts.spotify.com/api/token"

    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()
print(token)

def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token
    }

token = get_token()
