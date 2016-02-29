from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def index(request):
    # if user is authenticated route to normal index else route to login
    context = {}
    if request.user.is_authenticated():
        return render(request, 'index.html', context)
    return redirect(reverse('accounts:accounts-login'))
