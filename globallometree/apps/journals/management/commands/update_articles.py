from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from apps.journals.models import Journal
from apps.journals.models import Article
from datetime import datetime
from time import mktime
import feedparser

class Command(BaseCommand):
    help = 'Updates articles from RSS feeds'

    def handle(self, *args, **options):
        journals = Journal.objects.all()
        i = 0
        for journal in journals:
            feed = feedparser.parse(journal.feed_url)
            j = 0
            for entry in feed.entries:
                try: 
                    article = Article.objects.get(url = entry.link)
                except ObjectDoesNotExist:
                    try:
                        published = datetime.fromtimestamp(mktime(entry.published_parsed))
                    except AttributeError:
                        published = None
                    article = Article(
                        title = entry.title,
                        summary = entry.summary,
                        url = entry.link,
                        published = published,
                        journal = journal
                    )
                    # TODO: django.db.utils.DatabaseError: value too long for type character varying(200)
                    article.save()
                    i = i+1
                    j = j+1
            self.stdout.write('Imported {0} articles from {1}\n'.format(j, journal))
        self.stdout.write('Imported {0} articles in total\n'.format(i))