from django.shortcuts import render, redirect
from pyqie.qview.models import QueueItem

def home(request):
    tickets = QueueItem.objects.all()
    return render( request, "qview/home.html", {
        "tickets" : tickets
    })
