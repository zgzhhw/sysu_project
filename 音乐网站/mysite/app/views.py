from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import user_passes_test
from django.http import QueryDict
from urllib.parse import urlencode

'''from .models import Person
from .models import AudioFile
from .models import AudioFileForm
from .models import TCW_TQL'''

from app.models import *
from app.forms import * 
from datetime import datetime
# Create your views here.

def index(request):
    # 查询出Person对象信息，也就是数据表中的所有数据
    # 一行数据就是一个对象，一个格子的数据就是一个对象的一个属性值
    objs = Person.objects.all()

    # locals函数可以将该函数中出现过的所有变量传入到展示页面中，即index.html文件中
    return render(request,'index.html',locals())


def display_data(request):
    tcw_tql_data = TcwTql.objects.all()
    # 将数据传递给模板
    return render(request, 'tcw.html', {'tcw_tql_data': tcw_tql_data})

def query_person(request):
    if request.method == 'POST':
        # 处理查询请求
        name = request.POST.get('name', '')
        # 查询数据库中包含相应姓名的人员
        persons = AppPerson.objects.filter(name__icontains=name)
        return render(request, 'query_results.html', {'persons': persons})
    else:
        # 显示查询表单页面
        return render(request, 'query_form.html')



def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser)
def upload_audio(request):
    
    if request.method == 'POST':
        
        form = AudioFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            #return redirect('audio_list')  # 上传成功后跳转到音频列表页
    else:
        form = AudioFileForm()

    return render(request, 'upload_audio.html', {'form': form})

def query_singer(request):
    if request.method == 'POST':
        # 处理查询请求
        
        singer_name = request.POST.get('singer_name', '')
        if singer_name == '*':
            # 查询所有歌曲
            singers = Singers.objects.all()
        else:
            singers = Singers.objects.filter(singer_name__icontains=singer_name)
        (singer_name)
        # 查询数据库中包含相应歌手名的歌手
        singer_data = []
        
        for singer in singers:
            singer_data.append({'singer': singer})
        return render(request, 'query_singer_results.html', {'singers': singers})
    else:
        # 显示查询表单页面
        return render(request, 'query_singer_form.html')

# views.py

from django.shortcuts import render
from .models import Album

def query_album(request):
    if request.method == 'POST':
        album_name = request.POST.get('album_name', '')

        if album_name == '*':
            # 查询所有专辑
            albums = Album.objects.all()
        else:
            albums = Album.objects.filter(aname__icontains=album_name)

        album_data = []

        for album in albums:
            album_data.append({'album': album})

        return render(request, 'query_album_results.html', {'albums': album_data})
    else:
        # 显示查询表单页面
        return render(request, 'query_album_form.html')


from .models import Songs, Sing, Singers

def query_song(request):
    if request.method == 'POST':
        # 处理查询请求
        song_name = request.POST.get('sname', '')
        
        # 查询数据库中包含相应歌曲名的歌曲
        songs = Songs.objects.filter(sname__icontains=song_name)
        song_data = []
        
        for song in songs:
            # 获取与歌曲相关的所有 Sing 对象
            sings = Sing.objects.filter(sid=song.sid)
            audio_files = Audiofile.objects.filter(sname__icontains=song_name)
            # 获取歌手名字列表
            singer_ids = [sing.singer_id for sing in sings]
            (type(sings[0].sid))
            ("newbee!!!!!!!!")
            (type(singer_ids[0]),singer_ids[0])
            ("newbee!!!!!!!!")
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name',flat=True)
            
            #(sings)
            # 将歌手名字列表连接成一个字符串，用逗号分隔
            singer_names_str = ', '.join(singer_names)

            # 将歌曲和歌手名字信息添加到 song_data 列表中
            song_data.append({'song': song, 'singer_names': singer_names_str})
            (type(song_data))
        return render(request, 'query_song_results.html', {'songs': song_data})
    else:
        # 显示查询表单页面
        return render(request, 'query_song_form.html')



# views.py


# views.py - query_sing function

def query_sing(request):
    if request.method == 'POST':
        singer_name = request.POST.get('singer_name', '')

        if singer_name:
            # Query for the singer_id using the singer's name
            singer = Singers.objects.filter(singer_name__icontains=singer_name).values('singer_id').first()

            if singer:
                # Extract the singer_id value
                singer_id = singer['singer_id']

                # Query for the sid using the singer_id
                sings = Sing.objects.filter(singer_id=singer_id)
                sids = [sing.sid for sing in sings]

                # Query for all songs using the sid
                songs = Audiofile.objects.filter(id__in=sids)

                # Pass the results to the template
                song_data = []
                user = request.user
                song_id_arr=''
                for song in songs:
                    sings = Sing.objects.filter(sid=song.id)
                    collect = Collect.objects.filter(sid=song.id)
                    album_ids = [collec.aid for collec in collect]
                    singer_ids = [sing.singer_id for sing in sings]
                    singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
                    album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

                    singer_names_str = ', '.join(singer_names)
                    album_name_str = ', '.join(album_name)
                    #print(str(song.id))
                    song_id_arr = song_id_arr+','+str(song.id)
                
                    # 检查歌曲是否在用户的收藏夹中
                    is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

                    song_data.append({
                        'song': song,
                        'singer_names': singer_names_str,
                        'album_name': album_name_str,
                        'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
                    })
                song_id_arr = song_id_arr[1:]
                #print(song_id_arr)

                return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})
    
    # If no results or no search query, display the form
    return render(request, 'query_sing_form.html')

def query_collect(request):
    if request.method == 'POST':
        album_name = request.POST.get('album_name', '')

        if album_name:
            # Query for the album_id using the album's name
            album = Album.objects.filter(aname__icontains=album_name).values('aid').first()

            if album:
                # Extract the album_id value
                album_id = album['aid']

                # Query for the sid using the album_id
                collects = Collect.objects.filter(aid=album_id)
                sids = [collect.sid for collect in collects]

                # Query for all songs using the sid
                songs = Audiofile.objects.filter(id__in=sids)

                # Pass the results to the template
                song_data = []
                user = request.user
                song_id_arr=''
                for song in songs:
                    sings = Sing.objects.filter(sid=song.id)
                    collect = Collect.objects.filter(sid=song.id)
                    album_ids = [collec.aid for collec in collect]
                    singer_ids = [sing.singer_id for sing in sings]
                    singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
                    album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

                    singer_names_str = ', '.join(singer_names)
                    album_name_str = ', '.join(album_name)
                    #print(str(song.id))
                    song_id_arr = song_id_arr+','+str(song.id)
                
                    # 检查歌曲是否在用户的收藏夹中
                    is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

                    song_data.append({
                        'song': song,
                        'singer_names': singer_names_str,
                        'album_name': album_name_str,
                        'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
                    })
                song_id_arr = song_id_arr[1:]
                #print(song_id_arr)
                return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})
    else:
        return render(request, 'query_collect_form.html')


# views.py
def query_release(request):
    if request.method == 'POST':
        singer_name = request.POST.get('singer_name', '')

        if singer_name:
            # Query for the singer_id using the singer's name
            singer = Singers.objects.filter(singer_name__icontains=singer_name).values('singer_id').first()

            if singer:
                # Extract the singer_id value
                singer_id = singer['singer_id']

                # Query for the album_ids using the singer_id
                releases = Release.objects.filter(singer_id=singer_id)
                album_ids = [release.album_id for release in releases]

                # Query for all albums using the album_ids
                albums = Album.objects.filter(aid__in=album_ids)

                # Pass the results to the template
                return render(request, 'query_release_results.html', {'singer_name': singer_name, 'albums': albums})
    
    # If no results or no search query, display the form
    return render(request, 'query_release_form.html')


def query_audio(request):
    if request.method == 'POST':
        song_name = request.POST.get('name', '')
        if song_name == '*':
            songs = Audiofile.objects.all()
        else:
            songs = Audiofile.objects.filter(name__icontains=song_name)

        song_data = []
        user = request.user
        song_id_arr=''
        for song in songs:
            sings = Sing.objects.filter(sid=song.id)
            collect = Collect.objects.filter(sid=song.id)
            album_ids = [collec.aid for collec in collect]
            singer_ids = [sing.singer_id for sing in sings]
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
            album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

            singer_names_str = ', '.join(singer_names)
            album_name_str = ', '.join(album_name)
            #print(str(song.id))
            song_id_arr = song_id_arr+','+str(song.id)
        
            # 检查歌曲是否在用户的收藏夹中
            is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

            song_data.append({
                'song': song,
                'singer_names': singer_names_str,
                'album_name': album_name_str,
                'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
            })
        song_id_arr = song_id_arr[1:]
        #print(song_id_arr)

        return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})
    else:
        return render(request, 'query_audio_form.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # 重定向到主页
    return render(request, 'registration/login.html')

@login_required
def create_playlist(request):
    # 实现创建歌单的逻辑
    if request.method == 'POST':
        pl_name = request.POST.get('pl_name')
        tag = request.POST.get('tag')

        # 创建歌单对象
        new_playlist = Playlists(pl_name=pl_name, tag=tag, user=request.user)

        # 设置创建时间为当前时间
        new_playlist.cr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 保存歌单
        new_playlist.save()

        return render(request,'home.html')

    return render(request, 'playlists_form.html')

@login_required
def playlist_results(request):
    # 显示普通用户自己创建的歌单
    user_playlists = Playlists.objects.filter(user=request.user)
    return render(request, 'playlists_results.html', {'playlists': user_playlists})

@user_passes_test(lambda u: u.is_superuser)
def admin_playlist_results(request):
    # 只有管理员可以访问的歌单管理界面
    if not request.user.is_staff:
        # 如果不是管理员，重定向到普通用户的歌单页面
        return render(request,'login.html')

    all_playlists = Playlists.objects.all()
    return render(request, 'admin_playlists_results.html', {'playlists': all_playlists})

@login_required
def home(request):
    user_name = request.user.first_name  # 假设您的用户模型有get_full_name方法
    return render(request, 'home.html', {'user_name': user_name})

def host(request):  
    return render(request, 'host.html')










# views.py
from django.shortcuts import render, get_object_or_404
from .models import Playlists, Own, Audiofile
from django.http import HttpResponseRedirect
from django.urls import reverse

# views.py
from django.shortcuts import render, redirect
from .models import Playlists, Own

# views.py
from django.shortcuts import render, redirect
from .models import Audiofile, Playlists, Own

def add_to_playlist(request, song_id,song_id_array):
    user = request.user

    if request.method == 'POST':
        selected_playlist_id = request.POST.get('selected_playlist')
        if not Own.objects.filter(song_id=song_id, playlist_id=selected_playlist_id).exists():
            Own.objects.create(song_id=song_id, playlist_id=selected_playlist_id)
            playlist = Playlists.objects.get(pl_id=selected_playlist_id)
            if playlist.p_number is not None:
                playlist.p_number += 1
            else:
                # 如果 p_number 为 None，则将其设置为 1
                playlist.p_number = 1
            playlist.save()
        song_ids = [int(song_id) for song_id in song_id_array.split(',')]
        songs = Audiofile.objects.filter(id__in=song_ids)

        song_data = []
        user = request.user
        song_id_arr=''
        for song in songs:
            sings = Sing.objects.filter(sid=song.id)
            collect = Collect.objects.filter(sid=song.id)
            album_ids = [collec.aid for collec in collect]
            singer_ids = [sing.singer_id for sing in sings]
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
            album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

            singer_names_str = ', '.join(singer_names)
            album_name_str = ', '.join(album_name)
            #print(str(song.id))
            song_id_arr = song_id_arr+','+str(song.id)
        
            # 检查歌曲是否在用户的收藏夹中
            is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

            song_data.append({
                'song': song,
                'singer_names': singer_names_str,
                'album_name': album_name_str,
                'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
            })
        song_id_arr = song_id_arr[1:]
        #print(song_id_arr)

        return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})


    user_playlists = Playlists.objects.filter(user=user)
    song = Audiofile.objects.get(id=song_id)
    context = {'user_playlists': user_playlists, 'song': song,'song_id_array':song_id_array}
    return render(request, 'add_to_playlist.html', context)



def query_playlist(request, playlist_id):
    user = request.user

    # Retrieve the playlist object or return a 404 response if not found
    playlist = get_object_or_404(Playlists, pl_id=playlist_id)
    (request.method) 
    if request.method == 'GET':
        # You can remove this block if you don't need POST handling
        selected_playlist_id = request.POST.get('selected_playlist')
        songs_id = Own.objects.filter(playlist_id=playlist_id)
        songs = Audiofile.objects.filter(id__in=songs_id.values('song_id'))
        
        #(type(songs))
        song_data = []
        for song in songs:
            #(song)
            # 获取与歌曲相关的所有 Sing 对象
            sings = Sing.objects.filter(sid=song.id)
            collect = Collect.objects.filter(sid=song.id)
            #audio_files = Audiofile.objects.filter(name__icontains=song_name)
            singer_ids = [sing.singer_id for sing in sings]
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name',flat=True)
            
            # 将歌手名字列表连接成一个字符串，用逗号分隔
            singer_names_str = ', '.join(singer_names) 
            print("***")
            print(playlist.pl_id) 
            print("***")
            (singer_names_str)  
            song_data.append({'song': song, 'singer_names_str': singer_names_str})    
            
        context = {'playlist': playlist, 'song_data': song_data}
        #(song_data)


        return render(request, 'query_playlist.html', context)
    else:
        # Get the songs for the playlist
        songs = Audiofile.objects.filter(id__in=Own.objects.filter(playlist_id=playlist_id).values('song_id'))
        context = {'playlist': playlist, 'songs': songs}
        return render(request, 'query_playlist.html', context)



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Favorite
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

@login_required
def add_to_favorite(request, song_id,song_id_array):
    user = request.user
    return_to = reverse('home')
    if request.method == 'GET':
        if not Favorite.objects.filter(user_id=user.id, song_id=song_id).exists():
            Favorite.objects.create(user_id=user.id, song_id=song_id)
            # 获取最新的历史记录，如果没有历史记录，则返回到首页
        song_ids = [int(song_id) for song_id in song_id_array.split(',')]

        #id = Audiofile.objects.filter(id__in=song_ids).values_list('id', flat=True)
        
        
        songs = Audiofile.objects.filter(id__in=song_ids)

        song_data = []
        user = request.user
        song_id_arr=''
        for song in songs:
            sings = Sing.objects.filter(sid=song.id)
            collect = Collect.objects.filter(sid=song.id)
            album_ids = [collec.aid for collec in collect]
            singer_ids = [sing.singer_id for sing in sings]
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
            album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

            singer_names_str = ', '.join(singer_names)
            album_name_str = ', '.join(album_name)
            #print(str(song.id))
            song_id_arr = song_id_arr+','+str(song.id)
        
            # 检查歌曲是否在用户的收藏夹中
            is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

            song_data.append({
                'song': song,
                'singer_names': singer_names_str,
                'album_name': album_name_str,
                'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
            })
        song_id_arr = song_id_arr[1:]
        return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})
            
           
        return render(request, 'favor_fail.html', {'return_to': return_to})

@login_required
def delete_from_favorite(request, song_id,song_id_array):
    user = request.user
    return_to = reverse('home')
    if request.method == 'GET':
        if Favorite.objects.filter(user_id=user.id, song_id=song_id).exists():
            Favorite.objects.filter(user_id=user.id, song_id=song_id).delete()
            # 获取最新的历史记录，如果没有历史记录，则返回到首页

        #id = Audiofile.objects.filter(id__in=song_ids).values_list('id', flat=True)
        
        song_ids = [int(song_id) for song_id in song_id_array.split(',')]
        songs = Audiofile.objects.filter(id__in=song_ids)

        song_data = []
        user = request.user
        song_id_arr=''
        for song in songs:
            sings = Sing.objects.filter(sid=song.id)
            collect = Collect.objects.filter(sid=song.id)
            album_ids = [collec.aid for collec in collect]
            singer_ids = [sing.singer_id for sing in sings]
            singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
            album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

            singer_names_str = ', '.join(singer_names)
            album_name_str = ', '.join(album_name)
            #print(str(song.id))
            song_id_arr = song_id_arr+','+str(song.id)
        
            # 检查歌曲是否在用户的收藏夹中
            is_favorite = Favorite.objects.filter(user_id=user.id, song_id=song.id).exists()

            song_data.append({
                'song': song,
                'singer_names': singer_names_str,
                'album_name': album_name_str,
                'is_favorite': is_favorite,  # 添加是否在收藏夹中的信息                
            })
        song_id_arr = song_id_arr[1:]
        return render(request, 'query_audio_results.html', {'song_data': song_data,'song_id_arr':song_id_arr})
            
           
        return render(request, 'favor_fail.html', {'return_to': return_to})
from django.shortcuts import render
from .models import Favorite, Audiofile

def query_favorite(request):
    # 获取当前用户的 ID，你可能需要根据实际情况修改这里的获取方式
    current_user_id = request.user.id

    # 查询当前用户的 favorite 表中的歌曲
    user_favorites = Favorite.objects.filter(user_id=current_user_id)

    # 通过 favorite 表中的 song_id 查询对应的歌曲信息
    songs = Audiofile.objects.filter(id__in=user_favorites.values_list('song_id', flat=True))
    (songs)


    song_data = []
    for song in songs:
        sings = Sing.objects.filter(sid=song.id)
        collect = Collect.objects.filter(sid=song.id)
        album_ids = [collec.aid for collec in collect]
        singer_ids = [sing.singer_id for sing in sings]
        singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
        album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

        singer_names_str = ', '.join(singer_names)
        album_name_str = ', '.join(album_name)

        song_data.append({
            'song': song,
            'singer_names': singer_names_str,
            'album_name': album_name_str,
        })

    return render(request, 'query_favorite_results.html', {'song_data': song_data})
def delete_favorite_song(request, song_id):
    # Delete the song from the user's favorites
    current_user_id = request.user.id
    Favorite.objects.filter(user_id=current_user_id, song_id=song_id).delete()
    user_favorites = Favorite.objects.filter(user_id=current_user_id)

    # 通过 favorite 表中的 song_id 查询对应的歌曲信息
    songs = Audiofile.objects.filter(id__in=user_favorites.values_list('song_id', flat=True))
    (songs)


    song_data = []
    for song in songs:
        sings = Sing.objects.filter(sid=song.id)
        collect = Collect.objects.filter(sid=song.id)
        album_ids = [collec.aid for collec in collect]
        singer_ids = [sing.singer_id for sing in sings]
        singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
        album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

        singer_names_str = ', '.join(singer_names)
        album_name_str = ', '.join(album_name)

        song_data.append({
            'song': song,
            'singer_names': singer_names_str,
            'album_name': album_name_str,
        })

    return render(request, 'query_favorite_results.html', {'song_data': song_data})

def delete_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlists, pl_id=playlist_id)
    Own.objects.filter(playlist_id=playlist_id, song_id=song_id).delete()
    playlist.p_number -= 1
    
    playlist.save()
    playlist_songs = Own.objects.filter(playlist_id=playlist_id)
    # 通过 favorite 表中的 song_id 查询对应的歌曲信息
    songs = Audiofile.objects.filter(id__in=playlist_songs.values_list('song_id', flat=True))
    (songs)


    song_data = []
    for song in songs:
        sings = Sing.objects.filter(sid=song.id)
        collect = Collect.objects.filter(sid=song.id)
        album_ids = [collec.aid for collec in collect]
        singer_ids = [sing.singer_id for sing in sings]
        singer_names = Singers.objects.filter(singer_id__in=singer_ids).values_list('singer_name', flat=True)
        album_name = Album.objects.filter(aid__in=album_ids).values_list('aname', flat=True)

        singer_names_str = ', '.join(singer_names)
        album_name_str = ', '.join(album_name)

        song_data.append({
            'song': song,
            'singer_names': singer_names_str,
            'album_name': album_name_str,
        })

    context = {'playlist': playlist, 'song_data': song_data}
        #(song_data)


    return render(request, 'query_playlist.html', context)


def delete_playlist(request, playlist_id):
    user = request.user
    Playlists.objects.filter(pl_id=playlist_id, user=user).delete()
    Own.objects.filter(playlist_id=playlist_id).delete()
    user_playlists = Playlists.objects.filter(user=request.user)
    return render(request, 'playlists_results.html', {'playlists': user_playlists})