from login import *

client = yandex_login()
sp = spotify_login()

if credentials:
    save_credentials(credentials=credentials)
