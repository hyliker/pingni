#coding: utf-8
from django.contrib import admin
from person.models import *

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("user__username", )
    list_filter = ("gender", "is_noticed" )
    list_display = ("user", "nickname", "gender", "is_noticed", \
                    "followee_count", "follower_count", "show_count", \
                    "like_count", "visit_count")
admin.site.register(Profile, ProfileAdmin)

class FollowAdmin(admin.ModelAdmin):
    pass
admin.site.register(Follow, FollowAdmin)

