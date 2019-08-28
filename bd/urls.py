from django.conf.urls import patterns, url
from bd import views
from django.contrib import admin

urlpatterns = patterns(
    '', url(r'^$', views.index, name='index'),
    url(r'^gallery/', views.gallery, name='gallery'),
    url(r'^allmembers/', views.allmembers, name='allmembers'),
)