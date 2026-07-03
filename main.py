from funcs import *

# Проверка scopes
try:
    # Проверяем чтение плейлистов
    playlists = sp.current_user_playlists(limit=1)
    print("✅ Есть доступ к чтению плейлистов")
    
    # Проверяем создание плейлиста (создаём временный)
    test_playlist = sp.user_playlist_create(
        user=sp.current_user()['id'],
        name="TEST_DELETE_ME",
        public=False
    )
    print(f"✅ Есть доступ к созданию плейлистов (ID: {test_playlist['id']})")
    
    # Удаляем тестовый плейлист
    sp.current_user_unfollow_playlist(test_playlist['id'])
    print("✅ Тестовый плейлист удалён")
    
    print("\n🎉 Все права есть! Можно запускать перенос.")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("Нужно переавторизоваться с правильными scopes!")