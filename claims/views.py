import csv

import time
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect

from claims.forms import NewClaimForm, FilterClaimForm, UpdateClaimForm, FilterAuthoriseClaimForm
from claims.models import Claim, ClaimType
from profiles.models import EmployeeTimeRecorderUser


def new_claim(request):
    # if user is authenticated route to normal index else route to login

    context = {}
    if request.method == 'POST':
        form = NewClaimForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_claim = Claim.objects.create(owner=request.user,authorising_manager=data['authorising_manager'],
                                 type=data['type'], date = data['date'], claim_value=data['claim_value'])
            new_claim.save()#we need to save the valid claim
            return redirect(reverse('index'))
        pass
    else:
        try:
            inital_value = EmployeeTimeRecorderUser.objects.get(username=request.user.manager_email)
        except ObjectDoesNotExist:
            inital_value = None
        form = NewClaimForm(initial = {'authorising_manager' : inital_value})
    context["form"] = form
    return render(request, 'claims/new_claim.html', context)

def view_claims(request):
    # if user is authenticated route to normal index else route to login
    claims = Claim.objects.filter(owner=request.user).order_by('date')
    if request.method == 'POST':
        claim_filter = FilterClaimForm(request.POST.copy())
        claim_filter.is_valid()
        claims = Claim.objects.filter(owner=request.user).order_by('date')
        data = claim_filter.cleaned_data
        if data.get('authorised'):
            claims = claims.filter(authorised=True)
        if data.get('date_after'):
            claims = claims.filter(date__gt=data.get('date_after'))
        if data.get('date_before'):
            claims = claims.filter(date__lt=data.get('date_before'))
        if data.get('type'):
            claims = claims.filter(type=data.get('type'))
    else:
        claims = Claim.objects.filter(owner=request.user).order_by('date')
    paginator = Paginator(claims, 10) # Show 14 claimsnj per page
    page = request.GET.get('page')
    try:
        claims = paginator.page(page) if page else paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        claims = paginator.page(paginator.num_pages)
    claim_filter = {}
    claim_filter = FilterClaimForm()
    context = {'claims': claims, 'claim_filter': claim_filter}
    return render(request, 'claims/view_claims.html', context)

def view_claim(request, claim_id):
    # if user is authenticated route to normal index else route to login
    claim = Claim.objects.get(pk=claim_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            claim.delete()
            return redirect(reverse('index'))
        form = UpdateClaimForm(request.POST.copy(), claim_id=claim_id)
        if form.is_valid():
            data = form.cleaned_data
            claim.authorising_manager = data['authorising_manager']
            claim.type = data['type']
            claim.date = data['date']
            claim.claim_value = data['claim_value']
            claim.save()#we need to save the valid claim
            return redirect(reverse('index'))
    else:
        form = UpdateClaimForm(initial = {'authorising_manager' : claim.authorising_manager, 'date': claim.date,
                                    'type': claim.type, 'claim_value': claim.claim_value})
    context = {'form': form, 'claim': claim}
    return render(request, 'claims/view_claim.html', context)

def authorisation_claims(request):
    if request.method == 'POST':
        claim_ids = [key for key in request.POST if 'claim_id' == request.POST.get(key)]
        if claim_ids:
            for claim in Claim.objects.filter(id__in=claim_ids):
                if request.user.has_perm('claims.senior_authorise_claim') and claim.authorised:
                    claim.senior_authorised = True
                else:
                    claim.authorised = True
                claim.save()
        claim_filter = FilterAuthoriseClaimForm(request.POST.copy())
        claim_filter.is_valid()
        data = claim_filter.cleaned_data
        if data.get('other_manager'):
            claims = Claim.objects.filter(authorising_manager=data['other_manager'], authorised=False).order_by('date')
        else:
            if request.user.has_perm('claims.senior_authorise_claim'):
                claims = Claim.objects.filter(authorised=True, senior_authorised=False).order_by('date')
            else:
                claims = Claim.objects.filter(authorising_manager=request.user, authorised=False).order_by('date')
    else:
        if request.user.has_perm('claims.senior_authorise_claim'):
            claims = Claim.objects.filter(authorised=True, senior_authorised=False).order_by('date')
        else:
            claims = Claim.objects.filter(authorising_manager=request.user,
                                      authorised=False).order_by('date')
        claim_filter = {}
        claim_filter = FilterAuthoriseClaimForm()
    paginator = Paginator(claims, 10) # Show 10 claimsnj per page
    page = request.GET.get('page')
    try:
        claims = paginator.page(page) if page else paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        claims = paginator.page(paginator.num_pages)

    context = {'claims': claims, 'claim_filter': claim_filter}
    return render(request, 'claims/authorisation_claims.html', context)


def produce_report(request):
    '''
    Generate the CSV file for all authorised claims and save to disk..
    :param request:
    :return:
    '''
    CLAIM_TYPES = ClaimType.objects.values_list('name', flat=True).order_by('name')
    current_claim_owner = None
    csv_data_line = OrderedDict()
    def new_claim_owner(claim_owner):
        current_claim_owner = claim_owner
        csv_data_line = OrderedDict([('first_name', claim_owner.first_name), ('last_name', claim_owner.last_name),
                                    ('staff_number', claim_owner.staff_number)])
        for claim_type in CLAIM_TYPES:
            csv_data_line[claim_type] = 0
        return current_claim_owner, csv_data_line

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_claims{}.csv"'.format(time.strftime("%Y%m%d-%H%M%S"))
    writer = csv.writer(response)
    header_list = ['employee first name', 'employee last name', 'employee staff number']
    header_list += CLAIM_TYPES
    writer.writerow(header_list)
    for claim in Claim.objects.filter(senior_authorised=True, processed=False).order_by('owner'):
        if not claim.owner in [current_claim_owner]:
            if current_claim_owner: # this is not the first time:
                writer.writerow(csv_data_line.values)
            current_claim_owner, csv_data_line = new_claim_owner(claim.owner)
        csv_data_line[claim.type.name] += claim.claim_value
        claim.processed = True
        claim.save()
    if csv_data_line:
        writer.writerow(list(csv_data_line.values()))
    return response
