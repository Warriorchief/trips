from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$',views.success),
    url(r'^trip_items/(?P<trip_id>\d+)', views.showitem),
    url(r'^home$', views.success),
    url(r'^logout$', views.logout),
    url(r'^create$', views.createtrip),
    url(r'^addtrip/(?P<trip_id>\d+)', views.addtrip),
    url(r'^additem$', views.additem),
    ]
