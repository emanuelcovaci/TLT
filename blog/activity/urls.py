from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^activitati/$', views.activity, name='contact'),
    url(r'^post/(?P<slug>[^\.]+)/$', views.post, name='post'),

]
