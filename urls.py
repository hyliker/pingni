#coding: utf-8
from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from show.sitemap import ShowSitemap
sitemaps =  {
    "show": ShowSitemap,
}

urlpatterns = patterns('',
    # Example:
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^register/$', "person.views.register", name="regsiter"),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, "show_indexes": True}, ),
    (r'^$', 'show.views.show_new'),
    #(r'^$', 'show.views.index'),
    url(r'^settings/$', 'person.views.settings', name="settings"),
    url(r'^show/add/$', 'show.views.add_show', name="add_show"),
    url(r'^show/add_by_poster$', 'show.views.add_by_poster', name="show_add_by_poster"),
    url(r'^show/(?P<show_pk>\d+)/$', 'show.views.show', name="show"),
    url(r'^show/(?P<show_pk>\d+)/edit/$', 'show.views.edit_show', name="edit_show"),
    url(r'^show/(?P<show_pk>\d+)/comment/$', 'show.views.show', name="comment_show"),
    url(r'^show/user/(?P<user_pk>\d+)/$', 'show.views.show_user', name="show_user"),
    url(r'^show/user/$', 'show.views.show_user', name="show_my"),
    url(r'^show/user/(?P<user_pk>\d+)/likes/$', 'show.views.show_user_likes', name="show_user_likes"),
    url(r'^show/(?P<show_pk>\d+)/like/$', 'show.views.show_like', name="show_like"),
    url(r'^show/tag/(?P<tagname>.*)/$', 'show.views.show_tag', name="show_tag"),
    url(r'^show/tags/$', 'show.views.show_tags', name="show_tags"),
    url(r'^show/new/$', 'show.views.show_new', name="show_new"),
    url(r'^show/hot/$', 'show.views.show_hot', name="show_hot"),
    url(r'^show/sitemap/$', 'show.views.show_sitemap', name="show_sitemap"),
    url(r'^comment/add/$', 'commentit.views.add_comment', name="add_comment"),
    url(r'^comment/delete/(?P<comment_pk>\d+)$', 'commentit.views.delete_comment', name="delete_comment"),
    url(r'^person/following/(?P<user_pk>\d+)/$', 'person.views.following', name="following"),
    url(r'^person/following/(?P<user_pk>\d+)/undo/$', 'person.views.following', {"undo": True }, name="undo_following"),
    url(r'^person/follower/(?P<user_pk>\d+)/$', 'person.views.follower', name="follower"),
    url(r'^person/followee/(?P<user_pk>\d+)/$', 'person.views.followee', name="followee"),
    url(r'^person/password/change$', "person.views.password_change", name="password_change"),
    url(r'^captcha/', include('captcha.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
