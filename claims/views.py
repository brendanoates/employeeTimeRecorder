from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from claims.forms import ClaimForm
from claims.models import Claim
from profiles.models import EmployeeTimeRecorderUser


def new_claim(request):
    # if user is authenticated route to normal index else route to login

    context = {}
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_claim = Claim.objects.create(owner=request.user,authorising_manager=data['authorising_manager'],
                                 type=data['type'], date = data['date'], value=data['value'])
            new_claim.save()#we need to save the valid claim
            return redirect(reverse('index'))
        pass
    else:
        try:
            inital_value = EmployeeTimeRecorderUser.objects.get(username=request.user.manager_email)
        except ObjectDoesNotExist:
            inital_value = None
        form = ClaimForm(initial = {'authorising_manager' : inital_value})
    context["form"] = form
    return render(request, 'claims/new_claim.html', context)
