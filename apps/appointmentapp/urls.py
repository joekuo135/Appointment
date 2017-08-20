from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^validation$', views.validation),
    url(r'^login$', views.login),
    url(r'^welcome$', views.welcome),
    url(r'^add$', views.add),
    url(r'^update$', views.update),
    url(r'^logout$', views.logout),
    url(r'^edit/([0-9]+)/$', views.edit),
    url(r'^delete/([0-9]+)/$', views.delete),
]
