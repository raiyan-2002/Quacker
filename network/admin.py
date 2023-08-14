from django.contrib import admin
from .models import *
# Register your models here.

class FollowerAdmin(admin.ModelAdmin):
    filter_horizontal = ("following_list", )

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("posts", )

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Follower, FollowerAdmin)