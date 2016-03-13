from django.conf.urls import url

from claims import views

appname = 'claims'
urlpatterns = [
    url(r'^new_claim/', views.new_claim, name='new_claim'),
    url(r'^view_claim/(?P<claim_id>[0-9]+)/$', views.view_claim, name='view_claim'),
    url(r'^view_claims/', views.view_claims, name='view_claims'),
]
