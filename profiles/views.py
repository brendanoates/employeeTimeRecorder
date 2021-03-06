from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from profiles import logger


@login_required
def profile(request):
    context = {}
    if request.method == 'POST':
        # noinspection PyBroadException
        try:
            user = request.user
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
            if request.POST['staff_number']:
                user.staff_number = request.POST['staff_number']
            if request.POST['manager_email']:
                user.manager_email = request.POST['manager_email']
            user.save()
            return redirect(reverse('index'))
        except Exception:
            logger.exception('Exception')
            error = 'An Exception has occurred please report this if you continue to experience this issue'
            context['error'] = error
    return render(request, 'profiles/profile.html', context)
