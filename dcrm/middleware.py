import re
from django.conf import settings
from django.contrib.auth.middleware import LoginRequiredMiddleware

class CustomLoginRequiredMiddleware(LoginRequiredMiddleware):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.open_urls = [re.compile(url) for url in getattr(settings, "OPEN_URLS", [])]
        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        for url in self.open_urls:
            if url.match(request.path):
                return None  # Skip auth
        return super().process_view(request, view_func, view_args, view_kwargs)
