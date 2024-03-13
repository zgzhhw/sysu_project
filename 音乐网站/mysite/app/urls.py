from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('query/', query_person, name='query_person'),
    path('audio/', query_audio, name='query_audio'),
    path('upload/', upload_audio, name='upload_audio'),
    path('tcw/', display_data, name = 'display_data'),
    path('singers/',query_singer,name = 'query_singer'),
    path('songs/',query_song, name = 'query_song'),
    path('sing/',query_sing, name = 'query_sing'),
    path('album/',query_album, name = 'query_album'),
    path('collect/',query_collect, name = 'query_collect'),
    path('release/',query_release, name = 'query_release'),
    path('host/',host, name = 'host'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('home/', login_required(home), name='home'),
    path('create_playlist/', create_playlist, name='create_playlist'),
    path('playlists_results/', playlist_results, name='playlist_results'),
    path('admin_playlist_results/', admin_playlist_results, name='admin_playlist_results'),
    path('add_to_playlist/<int:song_id>/<str:song_id_array>', add_to_playlist, name='add_to_playlist'),
    
    path('query_playlist/<int:playlist_id>/', query_playlist, name='query_playlist'),
    path('add_to_favorite/<int:song_id>/<str:song_id_array>/', add_to_favorite, name='add_to_favorite'),
    path('query_favorite/', query_favorite, name='query_favorite'),
    path('delete_favorite_song/<int:song_id>/', delete_favorite_song, name='delete_favorite_song'),
    path('delete_from_favorite/<int:song_id>/<str:song_id_array>/', delete_from_favorite, name='delete_from_favorite'),
    path('delete_song_from_playlist/<int:playlist_id>/<int:song_id>/', delete_song_from_playlist, name='delete_song_from_playlist'),
    path('delete_playlist/<int:playlist_id>/', delete_playlist, name='delete_playlist'),
    #path('play/<int:song_id>/', play_song, name='play_song')
    # 其他URL配置...
]
