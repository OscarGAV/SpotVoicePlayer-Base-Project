"""
spotify_player.py
-----------------
Searches and plays a song on Spotify using the Spotipy API.
Requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URI
to be set in a .env file or as environment variables.
"""

import difflib
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SCOPE = "user-modify-playback-state user-read-playback-state"
REDIRECT_URI = "http://127.0.0.1:8888/callback"


def _get_client() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, redirect_uri=REDIRECT_URI))


def play_song(query: str) -> str:
    """
    Search for a song on Spotify and play it on the active device.
    Returns a status message.
    """
    try:
        sp = _get_client()
        results = sp.search(q=query, type="track", limit=5)
        tracks = results["tracks"]["items"]

        if not tracks:
            return f"No results found for '{query}' on Spotify."

        # Pick the track whose name+artist is most similar to the query
        candidates = [f"{t['name']} {t['artists'][0]['name']}".lower() for t in tracks]
        best_idx = difflib.get_close_matches(query.lower(), candidates, n=1, cutoff=0.0)
        idx = candidates.index(best_idx[0]) if best_idx else 0
        track = tracks[idx]

        track_name = track["name"]
        artist = track["artists"][0]["name"]
        uri = track["uri"]

        # Try to play on active device
        devices = sp.devices()
        active = next((d for d in devices["devices"] if d["is_active"]), None)

        if active:
            sp.start_playback(device_id=active["id"], uris=[uri])
            return f"Playing '{track_name}' by {artist} on Spotify."
        else:
            # No active device — open in browser as fallback
            url = track["external_urls"]["spotify"]
            webbrowser.open(url)
            return f"No active Spotify device. Opening '{track_name}' by {artist} in browser."

    except Exception as e:
        return f"Spotify error: {e}"