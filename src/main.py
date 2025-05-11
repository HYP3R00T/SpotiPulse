# spotify_api.py
from fastapi import FastAPI, HTTPException, Query
from src.auth import get_access_token
import requests

app = FastAPI()

BASE_URL = "https://api.spotify.com/v1/me"


def get_headers():
    return {"Authorization": f"Bearer {get_access_token()}"}


@app.get("/")
def root():
    return {"message": "Welcome"}


@app.get("/spotify/top-tracks")
def top_tracks():
    r = requests.get(f"{BASE_URL}/top/tracks?limit=10", headers=get_headers())
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return [
        {"name": t["name"], "artists": [a["name"] for a in t["artists"]], "uri": t["uri"]} for t in r.json()["items"]
    ]


@app.get("/spotify/now-playing")
def now_playing():
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=get_headers())
    if r.status_code == 204:
        return {"status": "No song currently playing"}
    elif r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    return {
        "name": data["item"]["name"],
        "artists": [a["name"] for a in data["item"]["artists"]],
        "is_playing": data["is_playing"],
    }


@app.get("/spotify/followed-artists")
def followed_artists():
    r = requests.get(f"{BASE_URL}/following?type=artist", headers=get_headers())
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return [artist["name"] for artist in r.json()["artists"]["items"]]


@app.post("/spotify/stop")
def stop_playback():
    r = requests.put("https://api.spotify.com/v1/me/player/pause", headers=get_headers())
    return (
        {"status": "Playback stopped"}
        if r.status_code == 204
        else HTTPException(status_code=r.status_code, detail=r.text)
    )


@app.post("/spotify/play")
def play(uri: str = Query(..., description="Spotify URI of the track to play")):
    body = {"uris": [uri]}
    r = requests.put("https://api.spotify.com/v1/me/player/play", headers=get_headers(), json=body)
    return (
        {"status": "Playback started"}
        if r.status_code in (204, 202)
        else HTTPException(status_code=r.status_code, detail=r.text)
    )
