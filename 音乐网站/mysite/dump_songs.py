import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()
from django.core.files import File
from django.utils import timezone
from app.models import Songs
# 打开音频文件并读取为二进制数据
with open("C:\\Users\\86191\\Music\\逃跑计划 - 再飞行.mp3", 'rb') as audio_file:
    binary_data = audio_file.read()

# 创建一个 Songs 实例
new_song = Songs(
    sname='再飞行',
    type='Pop',
    issue_time= '2014-01-01',

    duration='00:01:31',  # 时:分:秒
    audio=binary_data  # 插入二进制数据
)

# 保存实例到数据库
new_song.save()

