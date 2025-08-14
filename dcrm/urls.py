from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from scheduler.views import scheduler_inngest_view_path


def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),
    path('campaign/', include('campaign.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('clients.urls')),
    # path('posts/', include('posts.urls')),
]


urlpatterns += [scheduler_inngest_view_path]