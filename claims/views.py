from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from claims.forms import ClaimForm


def new_claim(request):
    # if user is authenticated route to normal index else route to login

    context = {}
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            return redirect(reverse('index'))
        pass
    else:
        form = ClaimForm()
    context["form"] = form
    return render(request, 'claims/new_claim.html', context)
