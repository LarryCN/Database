from django.conf.urls import patterns, url
from concert import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name = 'index'),
	url(r'^(?P<concert_id>\d+)/$', views.info, name = 'info'),
	url(r'^(?P<concert_id>\d+)/ratingdetail/$', views.ratingdetail, name = 'ratingdetail'),
	url(r'^(?P<concert_id>\d+)/like/$', views.like, name = 'like'),
	url(r'^(?P<concert_id>\d+)/reviews/$', views.reviews, name = 'reviews'),
	url(r'^(?P<concert_id>\d+)/ticket/$', views.ticket, name = 'ticket'),
)
