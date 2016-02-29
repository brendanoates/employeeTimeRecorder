from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views


def profile(request):
    return render(request, 'accounts/profile.html')


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
    # if user is authenticated route to normal index else route to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, reverse('index'))  # Redirect to index page.
            else:
                pass
                # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        pass

    form = AuthenticationForm()
    auth_logout(request)
    return render(request, 'accounts/register.html', {'form': form})


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



