from django.conf.urls import patterns, url
from artist import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name = 'index'),
	url(r'^(?P<artist_name_slug>[\w\-]+)/$', views.info, name = 'info'),
	url(r'^(?P<artist_name_slug>[\w\-]+)/postconcert/$', views.postconcert, name = 'postconcert'),
	url(r'^(?P<artist_name_slug>[\w\-]+)/edit/$', views.edit, name = 'edit'),
	url(r'^(?P<artist_name_slug>[\w\-]+)/follower/$', views.follower, name = 'follower'),
	url(r'^(?P<artist_name_slug>[\w\-]+)/selectstyle/$', views.selectstyle, name = 'selectstyle'),
)
