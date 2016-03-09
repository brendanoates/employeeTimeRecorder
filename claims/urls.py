from django.conf.urls import url

from claims import views

appname = 'claims'
urlpatterns = [
    url(r'^new_claim/', views.new_claim, name='new_claim'),
]
