#coding:utf-8
from django.conf.urls import patterns, url
from stock import views

urlpatterns = patterns('',

    # start to monitor
    url('^buy$', views.buy, name="buy"),

    # start to monitor
    url('^sell$', views.sell, name="sell"),

    # stop the thread
    url('^stop$', views.stop, name="stop"),
)
