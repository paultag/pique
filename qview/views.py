from django.shortcuts import render, redirect
from pique.qview.models import QueueItem

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

    return render( request, "qview/buginf.html", {
        "ticket" : ticket
    })
