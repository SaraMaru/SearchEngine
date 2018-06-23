from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path_to_term')

    def handle(self, *args, **options):
        pass
