from django.conf.urls import patterns, url
from lists import views

urlpatterns = patterns('',
                       url('', views.home_page),
                       )
