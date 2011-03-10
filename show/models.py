#coding: utf-8
import tagging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from common.stdimage import StdImageField
from commentit.models import Comment
from django.forms.fields import URLField
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals, F

class Show(models.Model):
    user = models.ForeignKey(User, verbose_name=u"帐号")
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = StdImageField(upload_to="show_photo", size=(800,600), thumbnail_size=(100,300), verbose_name=u"上传照片")
    image_url = models.URLField(blank=True, verbose_name=u"照片链接")
    description = models.TextField(max_length=256, blank=True, verbose_name=u"简短描述")
    quote = models.CharField(max_length=256, blank=True, verbose_name=u"引用")
    dtcreated = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name=u"创建日期")
    is_valid = models.NullBooleanField(verbose_name=u"是否合法", blank=True, help_text=u"审核此帖子是否存在不良内容")

    hits = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"采样数") 
    read_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"浏览数") 
    like_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"喜欢数")
    comment_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"评论数")

    comments = generic.GenericRelation(Comment)
    likes = models.ManyToManyField(User, null=True, blank=True, verbose_name=u"喜欢者", related_name="likes")

    def __unicode__(self):
        return u"%s" % self.title

    @property
    def quote_url(self):
        url = URLField()
        try:
            return url.clean(self.quote)
        except:
            return None

    @property
    def content_type(self):
        content_type = ContentType.objects.get_for_model(self)
        return content_type

    @property
    def tags_string(self):
        return ",".join([t.name for t in self.tags])

    @property
    def likit(self):
        return self.actions.filter(action="like")

    @property
    def likit_user_pks(self):
        return self.likit.values_list("user", flat=True)

    @models.permalink
    def get_absolute_url(self):
        return ("show", [str(self.pk)])

    def save(self, *args, **kwargs):
        super(Show, self).save(*args, **kwargs)
        profile = self.user.get_profile()
        profile.like_count = self.user.likes.count()
        profile.show_count = self.user.show_set.count()

        profile.save()
        return self

    def delete(self, *args, **kwargs):
        super(Show, self).delete(*args, **kwargs)
        profile = self.user.get_profile()
        profile.like_count = self.user.likes.count()
        profile.show_count = self.user.show_set.count()
        profile.save()

    class Meta:
        ordering = ["-dtcreated"]

tagging.register(Show)

def increase_photo_comment_count(sender, instance, signal, **kwargs):
    if instance.content_type.model_class() == Show:
        photo = Show.objects.get(pk=instance.object_id)
        photo.comment_count = F("comment_count") + 1
        photo.save()

def decrease_photo_comment_count(sender, instance, signal, **kwargs):
    if instance.content_type.model_class() == Show:
        photo = Show.objects.get(pk=instance.object_id)
        photo.comment_count = F("comment_count") - 1
        photo.save()

models.signals.post_save.connect(increase_photo_comment_count, sender=Comment)
models.signals.post_delete.connect(decrease_photo_comment_count, sender=Comment)

class ShowImage(models.Model):
    show = models.ForeignKey("Show")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = StdImageField(null=True, upload_to="show_showimage", size=(800,600), thumbnail_size=(100,300), verbose_name=u"上传照片")
    image_url = models.URLField()
    description = models.TextField()

    def __unicode__(self):
        return self.description

def update_show_image_url(sender, instance, signal, **kwargs):
    if not instance.show.image and not instance.show.image_url:
        instance.show.image_url = instance.image_url
    elif instance.modified < instance.show.dtcreated:
        instance.show.image_url = instance.image_url
    instance.show.save()

models.signals.post_save.connect(update_show_image_url, sender=ShowImage)
