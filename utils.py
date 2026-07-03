from usercreation import *

"""Функция для получения лайкнутых треков"""
def get_liked() -> list[ym.Track]:
    liked = client.users_likes_tracks()
    ids = [like.id for like in liked]
    tracks = client.tracks(ids)

    return tracks

"""Функция для получения треков из плейлиста по ссылке"""
def get_playlist(url:str) -> list[ym.Track]:
    uuid = url.split('/')[4]
    playlist = client.playlist(uuid)
    pkind = playlist.kind         
    uid = playlist.uid            
    playlist_title = playlist.title

    print(f"Название: {playlist_title}")
    print(f"kind: {pkind}")
    print(f"uid (user_id): {uid}")

    playlist = client.users_playlists(kind=pkind, user_id=uid)
    tracks = playlist.tracks
    ids = [track.id for track in tracks]
    tracks = client.tracks(ids)

    return tracks

"""Функция для получения информации об ОДНОМ треке"""
def get_track_info(track: ym.Track) -> dict:
    title = track.title
    artists = [artist['name'] for artist in track.artists]
    amart = len(artists)
    album_title = track.albums[0].title if track.albums else "Single"
    durms = track.duration_ms

    return {
        'title': title,
        'artists': artists, # списком
        'amart' : amart,
        'album_title': album_title,
        'durms': durms,

    }


"""==========================Функции Spotify=========================="""

"""Функция для поиска ОДНОГО трека"""
def search(track_name, artist_name) -> dict | None:
    query = f"{artist_name} {track_name}"
    print(f"Ищу трек {query}")
    res = sp.search(q=query, limit=1, type="track")
    if res and res['tracks']['items'][0]:
        track = res['tracks']['items'][0]
        artists = [artist['name'] for artist in track['album']['artists']]
        return {
            'id': track['id'],
            'album_title': track['album']['name'],
            'artists': artists,
            'amart' : len(artists),
            'durms' : track['duration_ms']
        }
    else:
        return None

"""Функция для валидации ОДНОГО трека"""
"""Добавляет инвалидные треки в структуру 1, валидные в структуру 2"""
def validate(ym_data:dict, sp_data:dict, invalid:dict, valid:list) -> None:
    ym_artists = ym_data.get('artists')
    sp_artists = sp_data.get('artists')
    ym_album = ym_data.get('album_title')
    sp_album = sp_data.get('album_title')
    ym_durms = ym_data.get('durms')
    sp_durms = sp_data.get('durms')

    sp_id = sp_data.get('id')

    mismatches = []

    if set(ym_artists) != set(sp_artists):
        mismatches.append(f'Различаются артисты: {ym_artists} - {sp_artists}')
    if ym_album != sp_album:
        mismatches.append(f'Различаются альбомы: {ym_album} - {sp_album}')
    if abs(ym_durms - sp_durms) >= 5000:
        mismatches.append(f'Различается длина: {ym_durms} - {sp_durms}')

    if len(mismatches) == 0:
        valid.append(sp_id)
    else:
        invalid[sp_id] = mismatches

""""Функция для плейлистов"""
def playlist(name:str, uid:str) -> str:
    playlists = sp.current_user_playlists()

    for playlist in playlists['items']:
        if playlist['name'].lower() == name.lower():
            print(f"Плейлист с именем {name} уже существует. Создать новый? (y/n)")
            answer = input().lower()
            if answer == "y":
                playlist = sp.user_playlist_create(user=uid, name=name, public=False)
                return playlist['id']
            else:
                return playlist['id']
    
    playlist = sp.user_playlist_create(user=uid, name=name, public=False)
    return playlist['id']
            
"""Функция подтверждения трека"""
"""Получает на вход треки, которые надо подтвердить, и добавляет id подтвержденных в лист"""
def confirm(invalid:dict, valid:list) -> None:
    for id in invalid:
        print("Неполное соответствие :")
        for mismatch in invalid[id]:
            print(mismatch)
        answer = input("Хотите добавить трек с такими несоответствиями? (y/n)").lower()
        if answer == "y":
            valid.append(id)
        
def transfer(playlist_id: str, track_ids: list) -> None:
    total = len(track_ids)
    if total == 0:
        print("⚠️ Нет треков для добавления!")
        return
    
    print(f"\n➕ Добавление {total} треков в плейлист...")
    
    chunk_size = 10
    for i in range(0, total, chunk_size):
        chunk = track_ids[i:i+chunk_size]
        sp.playlist_add_items(playlist_id=playlist_id, items=chunk)
        
        # Прогресс
        added = min(i + chunk_size, total)
        print(f"\r   Прогресс: {added}/{total} треков добавлено", end='', flush=True)
    
    print(f"\n✅ Все {total} треков перенесены!")