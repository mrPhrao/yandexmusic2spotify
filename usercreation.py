from login import *

client = yandex_login()
sp = spotify_login()

save_credentials(credentials=credentials)
