from django.conf.urls import patterns, url
from member import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name = 'index'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^home/$', views.home, name = 'home'),
	url(r'^(?P<user_name_slug>[\w\-]+)/$', views.homepage, name = 'homepage'),
	url(r'^(?P<user_name_slug>[\w\-]+)/edit/$', views.edit, name = 'edit'),
	url(r'^(?P<user_name_slug>[\w\-]+)/follower/$', views.follower, name = 'follower'),
	url(r'^(?P<user_name_slug>[\w\-]+)/selectstyle/$', views.selectstyle, name = 'selectstyle'),
	url(r'^(?P<user_name_slug>[\w\-]+)/recommendation/$', views.recommendation, name = 'recommendation'),
	url(r'^(?P<user_name_slug>[\w\-]+)/missingconcert/$', views.missingconcert, name = 'missingconcert'),
	url(r'^(?P<user_name_slug>[\w\-]+)/(?P<recommendation_id>\d+)/$', views.recommendationdetail, name = 'recommendationdetail'),
	url(r'^(?P<user_name_slug>[\w\-]+)/(?P<recommendation_id>\d+)/add_review/$', views.add_review, name = 'add_review'),
	url(r'^(?P<user_name_slug>[\w\-]+)/(?P<recommendation_id>\d+)/add_concert/$', views.add_concert, name = 'add_concert'),
)
