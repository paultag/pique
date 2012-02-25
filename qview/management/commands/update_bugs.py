from django.core.management.base import BaseCommand, CommandError
from pyqie.qview.models import QueueItem

import SOAPpy

"""
Cron-job

{
    'fixed_versions': [],
    'blockedby': '',
    'owner': '',
    'done': '',
    'unarchived': '',
    'keywords': '',
    'id': 658834,
    'subject': 'RFS: jabber-querybot -- Modular xmpp/jabber bot',
    'archived': 0,
    'forwarded': '',
    'bug_num': 658834,
    'msgid': '<20120206103322.31393.47245.reportbug@mbalmer.nine.ch>',
    'source': '',
    'location': 'db-h',
    'pending': 'pending',
    'found_date': [],
    'originator': 'Marco Balmer <marco@balmer.name>',
    'blocks': '',
    'tags': '',
    'last_modified': 1328534120,
    'date': 1328524562,
    'mergedwith': '',
    'severity': 'normal',
    'package': 'sponsorship-requests',
    'summary': '',
    'log_modified': 1328534120,
    'fixed_date': [],
    'found_versions': [],
    'affects': '',
    'found': '',
    'fixed': ''
}
"""

url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
namespace = 'Debbugs/SOAP'
server = SOAPpy.SOAPProxy(url, namespace)

package_name = "sponsorship-requests"

def get_info_on_bugs(bugs):
    """ Get all the active bugs we care about """
    return server.get_status(bugs)

def get_all_bugs():
    """ Get all the active bugs we care about """
    return get_info_on_bugs(server.get_bugs("package", package_name))

def clean_email(email):
    """ Clean an email so we just have the address """
    try:
        idex1 = email.index("<")
        idex2 = email.index(">")
        return email[idex1+1:idex2].strip()
    except ValueError:
        return email

def get_or_create_row( bugno ):
    """ Either get the record in the DB, or add a new record """
    bug = None
    try:
        bug = QueueItem.objects.get(bugno=bugno)
    except QueueItem.DoesNotExist:
        bug = QueueItem( bugno=bugno )
    return bug

def update_db(payload):
    """ Update all the bugs from the database """
    for bug in payload['item']:
        metainf = bug['value']
        print metainf
        b = get_or_create_row(metainf['bug_num'])
        b.active   = (metainf['done'] == '')
        b.reporter =  clean_email(metainf['originator'])
        b.owner    =  clean_email(metainf['owner'])
        b.subject  =  metainf['subject']
        b.severity =  metainf['severity']
        b.save()

def import_new_bugs():
    """ Import new bugs """
    bugs = get_all_bugs()
    update_db(bugs)

def refresh_db():
    """ Refresh the bugs in the database """
    tickets = QueueItem.objects.filter(
        active=True
    ).order_by('bugno')
    request_queue = []
    for ticket in tickets:
        request_queue.append(ticket.bugno)
    update_db(get_info_on_bugs(request_queue))

class Command(BaseCommand):
    args = ''
    help = 'Import all the bugs'

    def handle(self, *args, **options):
        self.stdout.write("Importing new bugs\n")
        import_new_bugs()
        self.stdout.write("Refreshing old bugs\n")
        refresh_db()
        return
