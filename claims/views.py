from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
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

def view_claims(request):
    # if user is authenticated route to normal index else route to login
    claims = Claim.objects.filter(owner=request.user).order_by('date')
    paginator = Paginator(claims, 10) # Show 14 claimsnj per page
    page = request.GET.get('page')
    try:
        claims = paginator.page(page) if page else paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        claims = paginator.page(paginator.num_pages)
    context = {'claims': claims}
    return render(request, 'claims/view_claims.html', context)

def view_claim(request, claim_id):
    # if user is authenticated route to normal index else route to login
    claim = Claim.objects.get(pk=claim_id)
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            claim.authorising_manager = data['authorising_manager']
            claim.type = data['type']
            claim.date = data['date']
            claim.value = data['value']
            claim.save()#we need to save the valid claim
            return redirect(reverse('index'))
        pass
    else:
        form = ClaimForm(initial = {'authorising_manager' : claim.authorising_manager, 'date': claim.date,
                                    'type': claim.type, 'value': claim.value})
    context = {'form': form}
    return render(request, 'claims/view_claim.html', context)
