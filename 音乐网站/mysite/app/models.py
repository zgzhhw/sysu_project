# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django import forms
from django.contrib.auth.models import User


class Audiofile(models.Model):
    name = models.CharField(max_length=50)
    audio_file = models.FileField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    issue_time = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)  # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'audiofile'

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = Audiofile
        fields = ['name', 'audio_file', 'type', 'issue_time', 'duration']



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TcwTql(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tcw_tql'

class Singers(models.Model):
    singer_id = models.IntegerField(primary_key=True, auto_created=True)
    singer_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'singers'


class Songs(models.Model):
    sid = models.IntegerField(primary_key=True, auto_created=True)
    sname = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    issue_time = models.DateTimeField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    audio = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'songs'

class Sing(models.Model):
    sid = models.IntegerField(primary_key=True)
    singer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sing'
        unique_together = (('sid', 'singer_id'),)

class Album(models.Model):
    aid = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=100)
    snumber = models.IntegerField(blank=True, null=True)
    release_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album'

class Playlists(models.Model):
    pl_id = models.AutoField(primary_key=True)
    pl_name = models.CharField(max_length=255)
    cr_time = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    p_number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'playlists'


class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    uname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'

class Collect(models.Model):
    aid = models.IntegerField(primary_key=True)
    sid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collect'
        unique_together = (('aid', 'sid'),)

class CollectAlbum(models.Model):
    user_id = models.IntegerField(primary_key=True)
    album_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collect_album'
        unique_together = (('user_id', 'album_id'),)

class CollectPlaylist(models.Model):
    user_id = models.IntegerField(primary_key=True)
    play_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'collect_playlist'
        unique_together = (('user_id', 'play_id'),)

class Download(models.Model):
    user_id = models.IntegerField(primary_key=True)
    song_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'download'
        unique_together = (('user_id', 'song_id'),)



class Own(models.Model):
    id=models.AutoField(primary_key=True)
    song_id = models.IntegerField()
    playlist_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'own'
        unique_together = (('song_id', 'playlist_id'),)

class Release(models.Model):
    album_id = models.IntegerField(primary_key=True)
    singer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'release'
        unique_together = (('album_id', 'singer_id'),)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # 区分管理员和普通用户
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True)  # 添加 email 字段


    class Meta:
        managed = False
        db_table = 'app_userprofile'
    # 其他字段...''

class Favorite(models.Model):
    fid=models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    song_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'favorite'
        #unique_together = (('user_id', 'song_id'),)