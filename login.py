import os
import json
import yandex_music as ym
from yandex_music.exceptions import UnauthorizedError, BadRequestError
import spotipy as spp

storage = 'data.json'
credentials = {}

def validate_json(data: dict):
    errors = []

    token = data.get('TOKEN', None)
    if not token:
        errors.append('NO TOKEN')
    client_id = data.get('CLIENT_ID', None)
    if not client_id:
        errors.append('NO CLIENT_ID')
    client_secret = data.get('CLIENT_SECRET', None)
    if not client_secret:
        errors.append('NO CLIENT_SECRET')

    return errors

def load_credentials() -> dict | None:
    if not os.path.exists(storage):
        return None
    try:
        with open(storage, 'r', encoding='utf-8') as file:
            data = json.load(file)
            errors = validate_json(data=data)
            if errors == []:
                return data
            else:
                print("⚠️  Файл с данными повреждён. Будет запрошен новый ввод.")
                return None
    except (json.JSONDecodeError, ValueError):
        print("⚠️  Файл с данными повреждён. Будет запрошен новый ввод.")
        return None
    
def save_credentials(credentials: dict) -> None:
    with open(storage, 'w', encoding='utf-8') as file:
        json.dump(credentials, file)
    print("✅ Данные сохранены!")

def yandex_login() -> ym.Client:
    print("Авторизация Яндекс музыки")
    data = load_credentials()
    
    if not data:
        while True:
            token = input("Введи OAuth токен Яндекс Музыки:\n").replace(' ', '')
            if not token:
                print("ПУСТОЙ ТОКЕН! Попробуй еще раз.")
                continue
            try:
                client = ym.Client(token=token)
                user = client.account_status().account.first_name
                print(f"✅ Авторизация Яндекс музыки успешна! Привет, {user}!\n")
                credentials['TOKEN'] = token
                return client
            except UnauthorizedError:
                print("❌ Неверный или истёкший токен! Попробуй снова.\n")
            except BadRequestError:
                print(f"❌ Ошибка запроса. Проверь правильность токена.\n")
            except Exception as e:
                print(f"❌ Неизвестная ошибка {e}! Попробуй еще раз")
    else:
        token = data.get('TOKEN')
        try:
            client = ym.Client(token=token)
            user = client.account_status().account.first_name
            print(f"✅ Авторизация по сохранённому токену! Привет, {user}!")
            return client
        except (UnauthorizedError, BadRequestError):
            print("⚠️ Сохранённый токен невалиден. Запрашиваю новый.")
            credentials.pop('TOKEN', None)
            return yandex_login()


def spotify_login() -> spp.Spotify:
    print("Авторизация Spotify App")
    data = load_credentials()

    redirect_uri = 'http://127.0.0.1:8888/callback'
    all_scopes = ( 
        'playlist-read-private playlist-read-collaborative '
        'playlist-modify-public playlist-modify-private '
        'user-library-read user-library-modify ugc-image-upload'
    )

    if not data:
        while True:
            client_id = input("Введи CLIENT_ID:\n").replace(' ','')
            if not client_id:
                print("⚠️ ПУСТОЙ ID! Попробуй еще раз.")
                continue
            client_secret = input("Введи CLIENT_SECRET:\n").replace(' ','')
            if not client_secret:
                print("⚠️ Пустой SECRET! Попробуй еще раз.")
                continue
            try:
                sp = spp.Spotify(
                    auth_manager=spp.oauth2.SpotifyOAuth(
                        client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope= all_scopes,
                    )
                )
                user = sp.current_user()
                print(f"✅ Авторизация Spotify успешна! Привет, {user['display_name']}!\n")
                credentials['CLIENT_ID'] = client_id
                credentials['CLIENT_SECRET'] = client_secret
                return sp
            
            except sp.exceptions.SpotifyException as e:
                if 'invalid_client' in str(e).lower():
                    print("❌ Неверный Client ID или Client Secret! Попробуй снова.\n")
                else:
                    print(f"❌ Ошибка Spotify.\n")
            
            except Exception as e:
                print(f"❌ Неизвестная ошибка.\n")

    else:
        try:
            sp = spp.Spotify(
                auth_manager=spp.oauth2.SpotifyOAuth(
                    client_id=data.get('CLIENT_ID'),
                    client_secret=data.get('CLIENT_SECRET'),
                    redirect_uri=redirect_uri,
                    scope=all_scopes,
                )
            )
            user = sp.current_user()
            print(f"✅ Авторизация по сохранённым данным! Привет, {user['display_name']}!\n")
            return sp
        
        except spp.exceptions.SpotifyException:
            print("⚠️ Сохранённые данные невалидны. Запрашиваю новые.")
            credentials.pop('CLIENT_ID', None)
            credentials.pop('CLIENT_SECRET', None)
            return spotify_login()  