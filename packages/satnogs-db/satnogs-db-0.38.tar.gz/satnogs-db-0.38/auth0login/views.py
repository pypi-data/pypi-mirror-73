"""SatNOGS DB Auth0 login module views"""
from __future__ import unicode_literals

from django.shortcuts import render


def index(request):
    """Returns the index view"""
    return render(request, 'index.html')
