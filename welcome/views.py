import socket
from django.shortcuts import render
# from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

# Create your views here.


def index(request):
    hostname = socket.gethostname()
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })


def health(request):
    return HttpResponse(PageView.objects.count())
