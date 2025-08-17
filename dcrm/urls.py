from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render

from scheduler.views import scheduler_inngest_view_path


def redirect_to_login(request):
    return redirect('login')

def home_view(request):
    """Feedback and feature requests page"""
    return render(request, "home/landing.html")

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('campaign/', include('campaign.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('clients.urls')),
    path('support/', include('support.urls')),
    # path('posts/', include('posts.urls')),
]


urlpatterns += [scheduler_inngest_view_path]