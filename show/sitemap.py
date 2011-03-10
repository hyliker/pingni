#coding: utf-8
from django.contrib.sitemaps import Sitemap
from show.models import Show

class ShowSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0 

    def items(self):
        return Show.objects.all()

    def lastmod(self, obj):
        return obj.dtcreated
