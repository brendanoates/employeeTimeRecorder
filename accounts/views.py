from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from accounts.forms import RegistrationForm
from profiles.models import EmployeeTimeRecorderUser


@login_required
def profile(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        staff_number = request.POST['staff_number']
        manager_email = '{}@amadeus.com'.format(request.POST['manager_email'])
        # try:
        #     manager = User.objects.get(email=manager_email)
        # except ObjectNotFound as e:
        #
        # manger
    return render(request, 'accounts/profile.html', context)


def login(request):
    # if user is authenticated route to normal index else route to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('index'))
            else:
                form = AuthenticationForm()
                context = {'error': "This account has been deactivated", 'form': form}
        else:
            form = AuthenticationForm()
            context = {'error': "Your username and password didn't match. Please try again.", 'form': form}
    else:
        form = AuthenticationForm()
        context = {'form': form}
        auth_logout(request)
    return render(request, 'accounts/login.html', context)


def register(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = None
        try:
            EmployeeTimeRecorderUser.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
        except IntegrityError as e:
            error = "This username has already been taken"
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('accounts:profile'))  # Redirect to profile page.
    form = RegistrationForm()
    context = {'form': form, 'error' : error}
    auth_logout(request)
    return render(request, 'accounts/register.html', context)


def logout(request):
    context = {'username': request.user.username}
    auth_logout(request)
    return render(request, 'accounts/logout.html', context)


def password_reset(request):
    return auth_views.password_reset(request, template_name='accounts/password_reset_form.html',
                                     email_template_name='accounts/password_reset_email.html',
                                     post_reset_redirect = reverse('accounts:password-reset-complete'))

def password_change(request):
    return auth_views.password_change(request, template_name='accounts/password_reset_form.html')

def password_change_done(request):
    return auth_views.password_change_done(request, template_name='accounts/password_reset_form.html')

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html', {})

def password_reset_complete(request):
    return auth_views.password_reset_complete(request, template_name='accounts/password_reset_done.html')

def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='accounts/password_reset_confirm.html',
                           ):
    return auth_views.password_reset_confirm(request, uidb64, token, template_name, post_reset_redirect='/')



