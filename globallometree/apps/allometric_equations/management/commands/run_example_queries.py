from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self,*args, **options):

        from globallometree.apps.allometric_equations import example_queries
