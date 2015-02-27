from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from artist.models import ArtistProfile
from member.models import UserProfile

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(selfself, request, user):
		member = UserProfile()
		member.user = user
		member.name = user.username
		member.slug = user.username
		member.save()
		return '/member/'

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'music.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^member/', include('member.urls')),
	url(r'^artist/', include('artist.urls')),
	url(r'^concert/', include('concert.urls')),
	url(r'^venue/', include('venue.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
