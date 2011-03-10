#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from common.stdimage import StdImageField

# Create your models here.
class Profile(models.Model):

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = (
        (GENDER_MALE, u'男'),
        (GENDER_FEMALE, u'女'),
    )

    user = models.ForeignKey(User, primary_key=True, verbose_name=u"帐号")
    nickname = models.CharField(max_length=64, blank=True, verbose_name=u"昵称")
    gender = models.CharField(max_length=2, blank=True, choices=GENDER_CHOICES, verbose_name=u"性别")
    avatar = StdImageField(upload_to="Profile_avatar", null=True, blank=True, \
                           size=(100,100, True), thumbnail_size=(36,36, True), \
                           verbose_name=u"上传头像", help_text=u"建议头像比例为:1:1")
    sign = models.CharField(max_length=128, blank=True, verbose_name=u"个性签名")
    location = models.CharField(max_length=32, blank=True, verbose_name=u"城市地区")
    website = models.URLField(blank=True, verbose_name=u"个人网站")
    is_noticed = models.NullBooleanField(blank=True, verbose_name=u"接受提醒邮件")

    followee_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"粉丝数") #我的粉丝,关注我的
    follower_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"关注数") #我关注的,我的关注
    show_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"分享数") #分享的show数目
    like_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"喜欢数") #喜欢收藏的show数目
    visit_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"人气数") #个人空站访问的show数目

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u"档案"
        verbose_name_plural = u"档案"

#def user_post_save(sender, instance, **kwargs):
    #profile, created = Profile.objects.get_or_create(user=instance)

#models.signals.post_save.connect(user_post_save, sender=User)

class Follow(models.Model):
    follower  =  models.ForeignKey(User, related_name="followers") #关系主动人
    followee = models.ForeignKey(User, related_name="followees") #关系被动人
    dtcreated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s, follow %s" % (self.follower, self.followee)

    class Meta:
        unique_together = (("follower", "followee"),)

    def save(self, *args, **kwargs):
        super(Follow, self).save(*args, **kwargs)
        follower_profile = self.follower.get_profile()
        follower_profile.followee_count = self.follower.followees.count()
        follower_profile.follower_count = self.follower.followers.count()
        follower_profile.save()

        followee_profile = self.followee.get_profile()
        followee_profile.followee_count = self.followee.followees.count()
        followee_profile.save()
        return self

    def delete(self, *args, **kwargs):
        super(Follow, self).delete(*args, **kwargs)
        follower_profile = self.follower.get_profile()
        follower_profile.followee_count = self.followee.followees.count()
        follower_profile.follower_count = self.follower.followers.count()
        follower_profile.save()

        followee_profile = self.followee.get_profile()
        followee_profile.followee_count = self.followee.followees.count()
        followee_profile.save()

#def increase_profile_followee_count(sender, instance, signal, **kwargs):
    #if instance.content_type.model_class() == Show:
        #photo = Show.objects.get(pk=instance.object_id)
        #photo.comment_count = F("comment_count") + 1
        #photo.save()

#def decrease_profile_follower_count(sender, instance, signal, **kwargs):
    #if instance.content_type.model_class() == Show:
        #photo = Show.objects.get(pk=instance.object_id)
        #photo.comment_count = F("comment_count") - 1
        #photo.save()

#models.signals.post_save.connect(increase_profile_followee_count, sender=Follow)
#models.signals.post_delete.connect(decrease_profile_follower_count, sender=Follow)
