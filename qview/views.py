from django.shortcuts import render, redirect
from pique.qview.models import QueueItem, Tag

from collections import defaultdict

def home(request):
    tickets = QueueItem.objects.filter(
        active=True
    ).order_by('bugno')

    return render( request, "qview/home.html", {
        "tickets" : tickets
    })

def buginf(request, buginf=None):
    ticket = QueueItem.objects.get(
        bugno=buginf
    )
    tags = Tag.objects.filter(
        bugno=buginf
    )
    from_org = ticket.reporter.split("@", 1)[1].replace(".", "_")
    return render( request, "qview/buginf.html", {
        "ticket"   : ticket,
        "from_org" : from_org,
        "tags"     : tags
    })
