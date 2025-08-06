from django.contrib import admin
from django.urls import path, include

from scheduler.views import scheduler_inngest_view_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('campaign/', include('campaign.urls')),
    path('api/', include('api.urls')),
    # path('posts/', include('posts.urls')),
]


urlpatterns += [scheduler_inngest_view_path]