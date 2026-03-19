# spotify_api.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# Get credentials from environment variables or use hardcoded (not recommended for production)
client_id = os.getenv("SPOTIFY_CLIENT_ID", "440c87dd56cf49bc838768900a710485")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "f05a325c1ee64e23a742752eba102b32")

# Initialize Spotify client
try:
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
    )
except Exception as e:
    sp = None
    print(f"Spotify initialization error: {e}")

def get_recommended_songs(emotion):
    """Get songs based on emotion/mood"""
    
    if sp is None:
        return []  # Return empty list if Spotify not initialized
    
    # Map emotions to Spotify playlist IDs
    playlist_map = {
        "happy": "37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
        "sad": "37i9dQZF1DX7qK8ma5wgG1",    # Sad Hour
        "neutral": "37i9dQZF1DX3rxVfibe1L0", # Chill Vibes
        "angry": "37i9dQZF1DX76Wlfdnj7AP",   # Rock Classics
        "surprise": "37i9dQZF1DX4WYpdgoIcn6", # Feel Good Friday
        "fear": "37i9dQZF1DX4o1oenSJRJd",    # All Out 80s
    }
    
    # Get playlist ID for the emotion, default to neutral
    playlist_id = playlist_map.get(emotion.lower(), playlist_map["neutral"])
    
    try:
        # Get playlist tracks
        results = sp.playlist_tracks(playlist_id, limit=15)
        
        songs = []
        for item in results['items']:
            track = item['track']
            if track:  # Check if track exists
                songs.append({
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "url": track['external_urls']['spotify']
                })
        
        return songs
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return []