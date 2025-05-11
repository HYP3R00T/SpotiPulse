import os
import requests
import base64
from urllib.parse import urlencode, urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

# Constants
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "https://hyperoot.dev/callback"
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-top-read user-follow-read streaming"
TOKEN_URL = "https://accounts.spotify.com/api/token"
AUTH_URL = "https://accounts.spotify.com/authorize"


# Step 1: Generate the authorization URL
def generate_auth_url():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return url


# Step 2: Exchange authorization code for tokens
def exchange_code_for_token(auth_code):
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code for token: {response.status_code} {response.text}")


# Step 3: Get the top 10 tracks
def get_top_ten_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks?limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks = response.json().get("items", [])
        return [f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}" for track in tracks]
    else:
        raise Exception(f"Failed to fetch top tracks: {response.status_code} {response.text}")


if __name__ == "__main__":
    # Step 1: Open the authorization URL in the browser
    print("Go to this URL and authorize:")
    auth_url = generate_auth_url()
    print(auth_url)

    # Step 2: Ask the user to paste the redirected URL
    redirected_url = input("Paste the full redirect URL here: ").strip()
    auth_code = parse_qs(urlparse(redirected_url).query).get("code", [None])[0]

    if not auth_code:
        print("Error: Authorization code not found in the URL.")
    else:
        try:
            # Exchange the authorization code for tokens
            tokens = exchange_code_for_token(auth_code)
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")

            print("Save this refresh token securely:", refresh_token)
            print(f"access_token = {access_token}")

            # Fetch and display the top 10 tracks
            top_tracks = get_top_ten_tracks(access_token)
            print("Your Top 10 Tracks:")
            for track in top_tracks:
                print(track)
        except Exception as e:
            print(f"Error: {e}")
