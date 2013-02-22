from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^/?$', views.index, name='index'),
    url(r'^/new$', views.new, name='new'),
    url(r'^/submit_new$', views.submit_new, name='submit_new'),
    url(r'^/(.+)/edit/?$', views.detail, {'template':'variants/edit.html'}, name='edit'),
    url(r'^/(.+)/submit_edit/?$', views.submit_edit, name='submit_edit'),
    url(r'^/(.+)/?$', views.detail, name='detail'),
)
