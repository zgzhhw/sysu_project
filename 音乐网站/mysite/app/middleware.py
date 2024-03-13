# middleware.py
from django.shortcuts import reverse

class HistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 在这里记录历史信息
        history = request.session.get('history', [])
        current_url = request.build_absolute_uri()
        if current_url not in history:
            history.append(current_url)
            request.session['history'] = history

        return response