from django.db import models
import feedparser

class Journal(models.Model):

	title = models.CharField(max_length=255)
	description = models.TextField()
	site_url = models.URLField()
	feed_url = models.URLField()

	def __unicode__(self):
		return self.title

	def title_upper(self):
	
		return self.title.upper()

	def feed_items(self):
		feed = feedparser.parse(self.feed_url)
		return feed