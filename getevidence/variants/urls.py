from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^/?$', views.index, name='index'),
    url(r'^/new/?$', views.new, name='new'),
    url(r'^/submit_new$', views.submit_new, name='submit_new'),
    url(r'^/(.+)/edit/?$', views.edit, name='edit'),
    url(r'^/(.+)/?$', views.detail, name='detail'),
)
