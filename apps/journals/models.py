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

    def title_upper(self):

        return self.title.upper()

    def feed_items(self):
        feed = feedparser.parse(self.feed_url)
        for i, entry in enumerate(feed.entries[:]):
            try:
                feed.entries[i].published_datetime = datetime.fromtimestamp(mktime(entry.published_parsed))
            except AttributeError:
                pass
        return feed
