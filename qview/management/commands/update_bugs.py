from django.core.management.base import BaseCommand, CommandError
from pyqie.qview.models import QueueItem

import SOAPpy

url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
namespace = 'Debbugs/SOAP'
server = SOAPpy.SOAPProxy(url, namespace)

package_name = "sponsorship-requests"

def get_all_bugs():
    return server.get_bugs("package", package_name)

class Command(BaseCommand):
    args = ''
    help = 'Import all the bugs'

    def handle(self, *args, **options):
        bugs = get_all_bugs()
        for bug in bugs:
            self.stdout.write(str(bug) + "\n")
