from django.contrib import admin

from .models import (
    Link, Post, PostsCampaign
)


admin.site.register(Link)
admin.site.register(Post)
admin.site.register(PostsCampaign)