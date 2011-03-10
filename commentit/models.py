#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Comment(models.Model):
    """简单通用的评论"""
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, blank=True) #允许匿名评论
    content = models.TextField(max_length=256)
    dtcommented = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return u"%s" % (self.author.username)

    class Meta:
        ordering = ["dtcommented"]
