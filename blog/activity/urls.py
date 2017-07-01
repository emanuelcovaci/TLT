from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^activitati/$', views.activity, name='contact'),
    url(r'^post/$', views.post, name='post'),

]
