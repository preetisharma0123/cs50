from django.contrib import admin

# Register your models here.

from .models import AbstractUser, Posts, Comment, Like, User, Following

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Following)
admin.site.register(Comment)
admin.site.register(Like)
