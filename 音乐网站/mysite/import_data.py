# import_data.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()

from app.models import Audiofile

# 批量导入数据
data = [
    {'name': '再飞行',
    'type':'Pop',
    'issue_time':'2014-01-01',
    'duration':'00:01:31',
    'audio_file': "C:\\Users\\86191\\Music\\逃跑计划 - 再飞行.mp3"},
    #{'name': 'Hymn For The Weekend', 'audio_file': "C:\\Users\\86191\\Music\\Alan Walker _ Coldplay - Hymn For The Weekend (Remix).mp3"},
    # 添加更多数据
]

for item in data:
    Audiofile.objects.create(**item)
