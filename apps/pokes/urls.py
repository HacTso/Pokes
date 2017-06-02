from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create), 
    url(r'^login_process$', views.login_process), 
    url(r'^pokes$', views.pokes), 
    url(r'^make_poke/(?P<user_id>\d+)/(?P<active_user_id>\d+)$', views.make_poke), 
    url(r'^logout$', views.logout), 
]