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

def detag(subject, tags=[]):
    try:
        sb = subject.index("[")
        eb = subject.index("]")
        tag = subject[sb+1:eb]
        nsub = subject[:sb] + subject[eb+1:]
        tags.append(tag)
        return detag(nsub, tags)
    except ValueError:
        subject = re.sub(r'\s+', ' ', subject)
        return ( subject, tags )

def yank_description(subject):
    subject = subject.replace(" - ", " -- ", 1)
    subject = subject.split(" -- ", 1)
    return ( subject[0], subject[1] )

def deprefix_subject(subject, pfxs=[]):
    try:
        ep = subject.index(":")
        if ep > 5:
            raise ValueError("Frack")
        pfxs.append( subject[:ep] )
        subject = subject[ep+1:].strip()
        return deprefix_subject(subject, pfxs)
    except ValueError:
        return subject, pfxs

def break_pkgname(name):
    try:
        nid = name.index("/")
        pkg  = name[:nid]
        vers = name[nid+1:]
        return ( pkg, vers )
    except ValueError:
        return ( name, None )

def process_subject(subject):
    subject, pfxs  = deprefix_subject(subject)
    subject, tags  = detag(subject)
    package, descr = yank_description(subject)
    pkg,     vers  = break_pkgname(package)
    return {
        "package" : pkg,
        "version" : vers,
        "descr"   : descr,
        "tags"    : ( pfxs + tags )
    }

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
        scraped_inf = process_subject( metainf['subject'] )
        metainf = bug['value']

        b = get_or_create_row(metainf['bug_num'])
        b.active   = (metainf['done'] == '')
        b.reporter =  clean_email(metainf['originator'])
        b.owner    =  clean_email(metainf['owner'])
        b.subject  =  metainf['subject']
        b.severity =  metainf['severity']
        # scraped info
        b.package  = scraped_inf['package']
        b.descr    = scraped_inf['descr']
        b.version  = scraped_inf['version']
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
