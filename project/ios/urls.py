#coding:utf-8
from django.conf.urls import patterns, url
from ios import views

urlpatterns = patterns('',

    # test
    url('^get_method$', views.get_method, name="get_method"),

    # post
    url('^post_method$', views.post_method, name="post_method"),

    # bill
    url('^bill$', views.showbill, name="showbill"),

    # add
    url('^add$', views.add, name="add"),
)
