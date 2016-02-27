from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    # if user is authenticated route to normal index else route to login
    context = {}
    if request.user.is_authenticated():
        return render(request, 'index.html', context)
    return render(request, 'login.html', context )