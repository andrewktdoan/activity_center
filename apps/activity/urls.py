from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^create_activity$', views.create_activity),
    url(r'^activity/(?P<act_id>\d+)/$', views.activity),
    url(r'^new_activity$', views.new_activity),
    url(r'^delete/(?P<act_id>\d+)/$', views.delete_activity),
    url(r'^join/(?P<act_id>\d+)/$', views.join_activity),
    url(r'^leave/(?P<act_id>\d+)/$', views.leave_activity),
    url(r'^logout$', views.logout),

]