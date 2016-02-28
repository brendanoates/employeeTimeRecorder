from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

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
                return render(request, './index.html', {})
            else:
                pass
                # Return a 'disabled account' error message
        else:
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
        auth_logout(request)
    return render(request, 'accounts/login.html', {'form': form,} )

def register(request):
    # if user is authenticated route to normal index else route to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, reverse('index')) # Redirect to index page.
            else:
                pass
                # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        pass

    form = AuthenticationForm()
    auth_logout(request)
    return render(request, 'accounts/login.html', {'form': form,} )

def logout(request):
    auth_logout(request)
    return login(request)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
        else:
            return render(request, 'registration/../templates/accounts/password.html', {'form': form,})