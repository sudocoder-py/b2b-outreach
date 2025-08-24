from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render

from scheduler.views import scheduler_inngest_view_path
from campaign.views import account_settings_view
from clients.views import home_view
from django.contrib.auth.decorators import login_not_required


def redirect_to_login(request):
    return redirect('login')


from django.db import connections
from django.http import HttpResponse
from django.db.utils import OperationalError

@login_not_required
def health_check(request):
    try:
        # Check database connectivity
        connections['default'].cursor()
        return HttpResponse("healthy", status=200)
    except OperationalError:
        return HttpResponse("unhealthy", status=503)


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('campaign/', include('campaign.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('clients.urls')),
    path('support/', include('support.urls')),
    path('feedback/', include('feedback.urls')),
    # path('posts/', include('posts.urls')),

    path('healthy/', health_check, name='health_check'),

    path('account-settings/', account_settings_view, name='account_settings'),
]


urlpatterns += [scheduler_inngest_view_path]