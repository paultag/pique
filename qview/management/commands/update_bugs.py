from django.core.management.base import BaseCommand, CommandError
from pyqie.qview.models import QueueItem

import SOAPpy

url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
namespace = 'Debbugs/SOAP'
server = SOAPpy.SOAPProxy(url, namespace)

package_name = "sponsorship-requests"

def get_all_bugs():
    return server.get_status(
        server.get_bugs("package", package_name)
    )

def clean_email(email):
    try:
        idex1 = email.index("<")
        idex2 = email.index(">")
        return email[idex1+1:idex2].strip()
    except ValueError:
        return email

class Command(BaseCommand):
    args = ''
    help = 'Import all the bugs'

    def handle(self, *args, **options):
        bugs = get_all_bugs()[0]
        for bug in bugs:
            metainf = bug['value']
            print metainf

            try:
                bug = QueueItem.objects.get(bugno=metainf['id'])
            except QueueItem.DoesNotExist:
                bug = QueueItem(
                    bugno=metainf['id']
                )
            bug.active   = (metainf['done'] == '')
            bug.reporter =  clean_email(metainf['originator'])
            bug.owner    =  clean_email(metainf['owner'])
            bug.subject  =  metainf['subject']
            bug.save()
