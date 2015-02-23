from django.db import models
from datetime import datetime
from time import mktime
import feedparser

class Journal(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    site_url = models.URLField()
    feed_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def latest_articles(self):
        return self.articles.order_by('-published')[:5]

    def recent_articles(self):
        return self.articles.order_by('-published')[:30]

class Article(models.Model):
    title       = models.CharField(max_length=510)
    summary     = models.TextField(null=True, blank=True)
    url         = models.URLField(max_length=400, unique=True)
    published   = models.DateTimeField(null=True)
    journal     = models.ForeignKey(Journal, related_name='articles')

    class Meta:
        ordering = ['-published']

    def __unicode__(self):
        return self.title


