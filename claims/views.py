from django.shortcuts import render

from claims.forms import ClaimForm


def new_claim(request):
    # if user is authenticated route to normal index else route to login
    context = {}
    form = ClaimForm()
    if request.method == 'POST':
        pass
    context["form"] = form
    return render(request, 'claims/new_claim.html', context)
