import yandex_music as ym
import spotipy as spp
from config import *
client = ym.Client(token=TOKEN)

all_scopes = (
    'playlist-read-private playlist-read-collaborative '
    'playlist-modify-public playlist-modify-private '
    'user-library-read user-library-modify ugc-image-upload'
)

sp = spp.Spotify(
    auth_manager=spp.oauth2.SpotifyOAuth(
        client_id=ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope= all_scopes,
    )
)