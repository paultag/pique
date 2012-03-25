from django.shortcuts import render, redirect
from pique.qview.models import QueueItem, Tag

import hashlib
from collections import defaultdict

def home(request):
    tickets = QueueItem.objects.filter(
        active=True
    ).order_by('bugno')

    return render( request, "qview/home.html", {
        "tickets" : tickets,
    })

def buginf(request, buginf=None):
    def hashmail(email):
        return hashlib.md5(email).hexdigest()

    ticket = QueueItem.objects.get(
        bugno=buginf
    )
    tags = Tag.objects.filter(
        bugno=buginf
    )
    from_org = ticket.reporter.split("@", 1)[1].replace(".", "_")

    reporter = hashmail(ticket.reporter)

    context = {
        "ticket"   : ticket,
        "from_org" : from_org,
        "tags"     : tags,
        "strtags"  : [ tag.name for tag in tags ],
        "rhash"    : reporter
    }

    if ticket.owner:
        owner = hashmail(ticket.owner)
        context['ohash'] = owner

    return render( request, "qview/buginf.html", context )
