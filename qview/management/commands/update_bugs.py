from django.core.management.base import BaseCommand, CommandError
from pyqie.qview.models import QueueItem

class Command(BaseCommand):
    args = ''
    help = 'Import all the bugs'

    def handle(self, *args, **options):
        self.stdout.write('Successfully closed poll\n')
