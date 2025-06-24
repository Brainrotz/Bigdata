import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# --- Spotify API Setup ---
SPOTIPY_CLIENT_ID = 'da0b004d279343678918db6298cf4129'
SPOTIPY_CLIENT_SECRET = '6c5808de18a44047912dd1fa4ad573f9'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

# --- Functions ---

def get_playlist_tracks(playlist_url):
    """Fetch track info (name, artist, ID) from a playlist"""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    try:
        results = sp.playlist_tracks(playlist_id)
        if not results or 'items' not in results:
            print("⚠️ No items found in playlist.")
            return []
    except Exception as e:
        print(f"❌ Error fetching playlist: {e}")
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
    """Get BPM (tempo) for a given track ID"""
    try:
        features = sp.audio_features([track_id])
        if features and features[0]:
            return features[0]['tempo']
    except Exception as e:
        print(f"⚠️ Error getting audio features for {track_id}: {e}")
    return None

def extract_bpm_from_playlist(playlist_url, output_csv="bpm_data.csv"):
    """Main function to extract BPMs and save to CSV"""
    print(f"🔍 Processing playlist: {playlist_url}")
    tracks = get_playlist_tracks(playlist_url)
    data = []

    for track in tracks:
        bpm = get_audio_features(track['id'])
        print(f"🎵 {track['name']} by {track['artist']} — BPM: {bpm}")
        data.append({
            'track': track['name'],
            'artist': track['artist'],
            'bpm': bpm
        })
        time.sleep(1)  # Respect rate limits

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ BPM data saved to: {output_csv}")

# --- Run Example ---

if __name__ == "__main__":
    playlist_url = "https://open.spotify.com/playlist/1WofXKQNJurvPfM1NglTMM"  # Replace this with your playlist
    extract_bpm_from_playlist(playlist_url, "happy_bpm_data.csv")
