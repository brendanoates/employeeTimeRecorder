"""employeeTimeRecorder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include, url
from accounts import views


appname = 'accounts'
urlpatterns = [
    url(r'^register/', views.register, name= 'accounts-register'),
    url(r'^profile/', views.profile, name= 'profile'),
    url(r'^login/', views.login, name= 'accounts-login'),
    url(r'^logout/', views.logout, name= 'accounts-logout'),
    url(r'^password_change/$', views.password_change, name='password-change'),
    url(r'^password_change/done/$', views.password_change_done, name='password-change_done'),
    url(r'^password_reset/', views.password_reset, name= 'password-reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password-reset-done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password-reset-confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password-reset-complete')








]