from utils import *

def data_gathering(tracklist) -> list:
    tracks_data = {}

    for id, track in enumerate(tracklist):
        tracks_data[id] = get_track_info(track=track)

    valid = []
    invalid = {}

    for id in tracks_data:
        artist = tracks_data[id].get('artists')[0] if tracks_data[id].get('artists') else ""
        sp_data = search(tracks_data[id].get('title'), artist)
        validate(tracks_data[id], sp_data=sp_data, invalid=invalid, valid=valid)
    
    confirm(invalid=invalid, valid=valid)
    return valid


def transfer_liked():
    liked_tracks = get_liked()
    valid = data_gathering(liked_tracks)
    if not valid:
        print("⚠️ Нет треков для добавления!")
        return

    try:
        ans = int(input("Добавить треки к лайкнутым, или создать новый плейлист? (1/2):"))
        if ans not in [1, 2]:
            print("❌ Неверный выбор. По умолчанию создаю плейлист.")
            ans = 2
    except ValueError:
        print("❌ Неверный ввод. По умолчанию создаю плейлист.")
        ans = 2
        
    if ans == 1:
        chunk_size = 100
        for i in range(0, len(valid), chunk_size):
            chunk = valid[i:i+chunk_size]
            sp.current_user_saved_tracks_add(tracks=chunk)
    elif ans == 2:
        playlist_name = input("Введите название плейлиста: ").strip()
        if not playlist_name:
            playlist_name = "Мне нравится (перенесённый)"
        playlist_id = playlist(name=playlist_name)
        transfer(playlist_id=playlist_id, track_ids=valid)


def transfer_playlist(playlist_url:str):
    tracks = get_playlist(playlist_url)
    valid = data_gathering(tracks)
    if not valid:
        print("⚠️ Нет треков для добавления!")
        return

    uuid = playlist_url.split('/')[4]
    playl1st = client.playlist(uuid)
    playlist_title = playl1st.title

    playlist_id = playlist(name=playlist_title)
    transfer(playlist_id=playlist_id, track_ids=valid)
