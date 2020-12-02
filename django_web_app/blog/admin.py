from django.contrib import admin
from .models import Post,Comments,GithubRespo

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(GithubRespo)

