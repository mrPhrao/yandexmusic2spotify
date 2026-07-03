import os
import yandex_music as ym
import spotipy as spp
from config import *

# Initialize Yandex Music client
client = ym.Client(token=TOKEN)

# Consolidated Spotify scopes
sc = (
    'user-library-read user-library-modify '
    'playlist-read-private playlist-read-collaborative '
    'playlist-modify-private playlist-modify-public'
)

# Initialize Spotify client
sp = spp.Spotify(
    auth_manager=spp.oauth2.SpotifyOAuth(
        client_id=ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=sc,
    )
)

print(f"Logged into Spotify as User ID: {sp.current_user()['id']}")

# Fetch first page of playlists
results = sp.current_user_playlists(limit=50)
playlists = results['items']

# Pagination loop
while results['next']:
    results = sp.next(results)
    playlists.extend(results['items'])

print(f"Total playlists found: {len(playlists)}")

# # Add a track to your liked songs
# sp.current_user_saved_tracks_add(tracks=['3R5b9BQcLAkraCbclYa591'])
