#coding: utf-8
from django.contrib import admin
from commentit.models import *

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "dtcommented"
    list_display = ("author", "content", "dtcommented")
    search_fields = ("content",)
    list_filter = ("dtcommented", )
admin.site.register(Comment, CommentAdmin)
