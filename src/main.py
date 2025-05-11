# spotify_api.py
from fastapi import FastAPI, HTTPException, Query
from src.auth import get_access_token
from src.spotify import generate_auth_url, exchange_code_for_token
import requests

app = FastAPI()

BASE_URL = "https://api.spotify.com/v1/me"


# Helper function to get headers
def get_headers():
    try:
        return {"Authorization": f"Bearer {get_access_token()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")


@app.get("/")
def root():
    return {"message": "Welcome"}


@app.get("/spotify/auth-url")
def get_auth_url():
    return {"auth_url": generate_auth_url()}


@app.post("/spotify/exchange-token")
def exchange_token(redirected_url: str):
    try:
        from urllib.parse import urlparse, parse_qs

        auth_code = parse_qs(urlparse(redirected_url).query).get("code", [None])[0]
        if not auth_code:
            raise HTTPException(status_code=400, detail="Authorization code not found in the URL.")
        tokens = exchange_code_for_token(auth_code)
        return {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange token: {str(e)}")


@app.get("/spotify/top-tracks")
def top_tracks():
    try:
        r = requests.get(f"{BASE_URL}/top/tracks?limit=10", headers=get_headers())
        r.raise_for_status()
        return [
            {"name": t["name"], "artists": [a["name"] for a in t["artists"]], "uri": t["uri"]}
            for t in r.json()["items"]
        ]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=str(e))


@app.get("/spotify/now-playing")
def now_playing():
    try:
        r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=get_headers())
        if r.status_code == 204:
            return {"status": "No song currently playing"}
        r.raise_for_status()
        data = r.json()
        return {
            "name": data["item"]["name"],
            "artists": [a["name"] for a in data["item"]["artists"]],
            "is_playing": data["is_playing"],
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=str(e))


@app.get("/spotify/followed-artists")
def followed_artists():
    try:
        r = requests.get(f"{BASE_URL}/following?type=artist", headers=get_headers())
        r.raise_for_status()
        return [artist["name"] for artist in r.json()["artists"]["items"]]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=str(e))


@app.post("/spotify/stop")
def stop_playback():
    try:
        r = requests.put("https://api.spotify.com/v1/me/player/pause", headers=get_headers())
        if r.status_code == 204:
            return {"status": "Playback stopped"}
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=str(e))


@app.post("/spotify/play")
def play(uri: str = Query(..., description="Spotify URI of the track to play")):
    try:
        body = {"uris": [uri]}
        r = requests.put("https://api.spotify.com/v1/me/player/play", headers=get_headers(), json=body)
        if r.status_code in (204, 202):
            return {"status": "Playback started"}
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=str(e))
