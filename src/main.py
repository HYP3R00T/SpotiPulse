# spotify_api.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from src.auth import get_access_token
import requests

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.spotify.com/v1/me"


# Helper function to get headers
def get_headers():
    try:
        return {"Authorization": f"Bearer {get_access_token()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get access token: {str(e)}")


@app.get("/")
def root():
    return {"message": "Welcome to SpotiPulse"}


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


@app.put("/player/pause")
def stop_playback_with_device(
    device_id: str = Query(
        None,
        description="The id of the device this command is targeting. If not supplied, the user's currently active device is the target.",
    ),
):
    """
    Stop playback on a specific device or the currently active device.
    """
    try:
        headers = get_headers()
        params = {"device_id": device_id} if device_id else {}

        r = requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers, params=params)

        if r.status_code == 204:
            return {"status": "Playback stopped"}
        elif r.status_code == 404:
            raise HTTPException(status_code=404, detail="No active device found to stop playback.")
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to stop playback: {str(e)}")


@app.put("/player/play")
def play_track_with_device(
    device_id: str = Query(
        None,
        description="The id of the device this command is targeting. If not supplied, the user's currently active device is the target.",
    ),
    context_uri: str = Query(
        None,
        description="Optional. Spotify URI of the context to play. Valid contexts are albums, artists & playlists.",
    ),
    uris: list[str] = Query(
        None,
        description="Optional. A JSON array of the Spotify track URIs to play.",
    ),
    position_ms: int = Query(
        None,
        description="Optional. Indicates the position in milliseconds to start playback.",
    ),
):
    """
    Start playback on a specific device or the currently active device.
    """
    try:
        headers = get_headers()
        data = {}

        if context_uri:
            data["context_uri"] = context_uri
        if uris:
            data["uris"] = uris
        if position_ms is not None:
            data["position_ms"] = position_ms

        params = {"device_id": device_id} if device_id else {}

        r = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, params=params, json=data)

        if r.status_code == 204:
            return {"status": "Playback started"}
        elif r.status_code == 404:
            raise HTTPException(status_code=404, detail="No active device found to start playback.")
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to start playback: {str(e)}")
