import requests
import os
import base64

from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
REDIRECT_URI = "https://hyperoot.dev/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"


# Function to get a new access token using the refresh token
def get_access_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise Exception(
            "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET. Please set them in your environment variables."
        )

    if not REFRESH_TOKEN:
        raise Exception("Missing SPOTIFY_REFRESH_TOKEN. Please set it in your environment variables.")

    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")
