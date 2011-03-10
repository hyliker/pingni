#coding: utf-8
from django.contrib import admin
from show.models import *

class ShowAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcreated"
    search_fields = ("user__username", "title")
    list_filter = ("is_valid", "dtcreated" )
    list_display = ("user", "title", "dtcreated", "hits", "read_count", "comment_count", "like_count", "is_valid")
admin.site.register(Show, ShowAdmin)

class ShowImageAdmin(admin.ModelAdmin):
    list_display = ("show", "description")

admin.site.register(ShowImage, ShowImageAdmin)
