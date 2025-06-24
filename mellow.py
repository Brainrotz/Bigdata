import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import requests
from colorthief import ColorThief
from io import BytesIO
import pandas as pd
import time

# --- SETUP APIS ---

# Spotify setup
SPOTIPY_CLIENT_ID = 'da0b004d279343678918db6298cf4129'
SPOTIPY_CLIENT_SECRET = '6c5808de18a44047912dd1fa4ad573f9'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

GENIUS_TOKEN = "rtmw6xSd7KMnFK3_nTTU4L_0VfYMVB6Q97POffogG8M7Ib_v7DbebZCwpUm7GnCY"
genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True, remove_section_headers=True)

# --- FUNCTIONS ---

def get_playlist_tracks(playlist_url):
    """Extracts all track info from a Spotify playlist"""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    try:
        results = sp.playlist_tracks(playlist_id)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []

    if not results or 'items' not in results:
        print("No tracks found.")
        return []

    tracks = []
    for item in results['items']:
        track = item.get('track')
        if track:
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'id': track['id']
            })
    return tracks

def get_audio_features(track_id):
    """Fetch BPM and other audio features"""
    try:
        response = sp.audio_features([track_id])
        if response and response[0]:
            return response[0].get('tempo')
        else:
            print(f"No audio features returned for {track_id}")
            return None
    except Exception as e:
        print(f"Error fetching audio features for {track_id}: {e}")
        return None

def get_album_art_url(track_name, artist_name, track_id):
    """Try Genius first, fallback to Spotify album art."""
    # Try Genius API first
    try:
        song = genius.search_song(title=track_name, artist=artist_name)
        if song and song.song_art_image_url:
            return song.song_art_image_url
        else:
            print(f"No Genius image for '{track_name}' by '{artist_name}'")
    except Exception as e:
        print(f"Genius API error for '{track_name}' by '{artist_name}': {e}")

     # Fallback to Spotify album art
    try:
        track_info = sp.track(track_id)
        if track_info and 'album' in track_info and 'images' in track_info['album']:
            images = track_info['album']['images']
            if images:
                return images[0]['url']
        print(f"No Spotify album art for track ID {track_id}")
    except Exception as e:
        print(f"Spotify API error for track ID {track_id}: {e}")


    return None

def get_dominant_color(image_url):
    """Download image and extract dominant color"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        img = BytesIO(response.content)
        color_thief = ColorThief(img)
        return color_thief.get_color(quality=1)  # RGB tuple
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error {response.status_code} for {image_url}: {http_err}")
    except Exception as e:
        print(f"Error processing image at {image_url}: {e}")
    return None

def process_playlist(playlist_url, mood_label):
    """Extract BPM and color data from a playlist"""
    print(f"Processing playlist: {mood_label}")
    tracks = get_playlist_tracks(playlist_url)
    data = []

    for track in tracks:
        print(f"Track: {track['name']} by {track['artist']}")
        bpm = get_audio_features(track['id'])
        art_url = get_album_art_url(track['name'], track['artist'], track['id'])
        color = get_dominant_color(art_url) if art_url else None

        data.append({
            'track': track['name'],
            'artist': track['artist'],
            'bpm': bpm,
            'art_url': art_url,
            'dominant_color': color,
            'mood': mood_label
        })
        time.sleep(2)  # avoid API rate limits

    return pd.DataFrame(data)

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    playlist_url = "https://open.spotify.com/playlist/5DbNSATdib0YNpThI8i7MA"
    df_mellow = process_playlist(playlist_url, "mellow")
    df_mellow.to_csv("mellow_playlist_data.csv", index=False)
    print(df_mellow.head())