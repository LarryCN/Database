from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from venue.models import Venue 
from concert.models import Concert

# Create your views here.
def index(request):
	venue_list = Venue.objects.all()[:]
	context_dict = {'venue': venue_list}

	response = render(request, 'venue/index.html', context_dict)

	return response

def info(request, venue_name_slug):
	context_dict = {}	

	try:
		venue = Venue.objects.get(slug = venue_name_slug)
		concerts = Concert.objects.filter(venue = venue)
		context_dict['venue'] = venue
		context_dict['concerts'] = concerts
	except Venue.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything - the template displays the "no category" message for us.
		pass	

	return render(request, 'venue/info.html', context_dict)
