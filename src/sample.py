import requests

from src.auth import get_access_token


# Step 3: Get the top 10 tracks
def get_top_ten_tracks():
    try:
        access_token = get_access_token()
    except Exception as e:
        raise Exception(f"Error fetching access token: {e}")

    url = "https://api.spotify.com/v1/me/top/tracks?limit=10"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks = response.json().get("items", [])
        return [f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}" for track in tracks]
    else:
        raise Exception(f"Failed to fetch top tracks: {response.status_code} {response.text}")


if __name__ == "__main__":
    try:
        # Fetch and display the top 10 tracks
        top_tracks = get_top_ten_tracks()
        print("Your Top 10 Tracks:")
        for track in top_tracks:
            print(track)
    except Exception as e:
        print(f"Error: {e}")
