from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from artist.models import ArtistProfile, ArtistStyle, Fan
from artist.forms import ArtistProfileForm, ConcertForm, FanForm
from venue.models import Venue
from django.utils import timezone
from member.forms import StyleForm
from member.models import Style, UserProfile, SubCategory
from concert.models import Concert
from django.db.models import Avg, Sum
from django.contrib.auth.decorators import login_required
from concert.views import POST_BY_ARTIST 

# Create your views here.
@login_required
def follower(request, artist_name_slug):
	try:
		artist = ArtistProfile.objects.get(slug = artist_name_slug)
		context_dict = {}
		context_dict['artist'] = artist
		fans = Fan.objects.filter(artist_id = artist).select_related('user_id')
		context_dict['fans'] = fans
		return render(request, 'artist/follower.html', context_dict)
	except ArtistProfile.DoesNotExist:
		pass
	return HttpResponse("No such artist here")
	

def index(request):
	artist_list = ArtistProfile.objects.all()[:]
	context_dict = {'artists': artist_list}

	response = render(request, 'artist/index.html', context_dict)

	return response

def info(request, artist_name_slug):
	context_dict = {}	
	try:
		artist = ArtistProfile.objects.get(slug = artist_name_slug)
		context_dict['is_artist'] = False
		if request.user == artist.artist:
			context_dict['is_artist'] = True
		concert = Concert.objects.filter(artist_id = artist)
		context_dict['artist'] = artist
		context_dict['concerts'] = concert
		context_dict['is_user'] = False
		fans = Fan.objects.filter(artist_id = artist).count()
		context_dict['fans'] = fans
		style = ArtistStyle.objects.all().select_related('style_id')
		is_null = SubCategory.objects.get(name = 'null')
		styles = ''
		for s in style:
			if s.style_id.sub_category == is_null:
				styles += str(s.style_id.category.name) + '   '
			else:
				styles += (str(s.style_id.category.name) + '-' + str(s.style_id.sub_category.name)) + ' '
		context_dict['styles'] = styles
		try:
			member = UserProfile.objects.filter(user = request.user)			
			if member:
				context_dict['is_user'] = True
				context_dict['is_fan'] = False
				member = UserProfile.objects.get(user = request.user)
				fan = Fan.objects.filter(user_id = member, artist_id = artist)
				if fan:
					context_dict['is_fan'] = True
				if request.method == 'POST' and not context_dict['is_fan']:
					form = FanForm(request.POST)
					
					if form.is_valid():
						user = form.save(commit = False)
						tmp = Fan()
						tmp.time = timezone.now()
						tmp.user_id = member
						tmp.artist_id = artist
						tmp.save()
						return info(request, artist_name_slug)
				else:
					form = FanForm()
				context_dict['form'] = form
		except:
			pass
	except ArtistProfile.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything - the template displays the "no category" message for us.
		pass

	return render(request, 'artist/info.html', context_dict)

def postconcert(request, artist_name_slug):
	try:
		artist = ArtistProfile.objects.get(slug = artist_name_slug)
		context_dict = {}
		if request.user == artist.artist:
			context_dict['artist'] = artist
			if request.method == 'POST':
				form = ConcertForm(request.POST)
	
				if form.is_valid():
					concert = form.save(commit = False)
					concert.artist_id = artist
					concert.post_time = timezone.now()
					concert.remark_state = POST_BY_ARTIST
					concert.save()
					return info(request, artist_name_slug)
				else:
					print form.errors
			else:
				form = ConcertForm()
			context_dict['form'] = form
			return render(request, 'artist/postconcert.html', context_dict)
		else:
			return HttpResponse("Only the artist could post a new concert.")
	except ArtistProfile.DoesNotExist:
		pass
	return HttpResponse("No such artist here")

def edit(request, artist_name_slug):
	try:
		artist = ArtistProfile.objects.get(slug = artist_name_slug)
		if request.user == artist.artist:
			context_dict = {}
			context_dict['artist'] = artist
			if request.method == 'POST':
				form = ArtistProfileForm(request.POST, request.FILES)
	
				if form.is_valid():
					artistprofile = form.save(commit = False)
					artist.websit = artistprofile.websit
					artist.bio = artistprofile.bio
					artist.picture = artistprofile.picture
					artist.save()
					return info(request, artist_name_slug)
				else:
					print form.errors
			else:
				form = ArtistProfileForm()
			context_dict['form'] = form
			return render(request, 'artist/edit.html', context_dict)
		else:
			return HttpResponse("Only the artist could edit the information.")
	except ArtistProfile.DoesNotExist:
		pass
	return HttpResponse("No such artist here")

def selectstyle(request, artist_name_slug):
	try:
		artist = ArtistProfile.objects.get(slug = artist_name_slug)
		if request.user == artist.artist:
			context_dict = {}
			context_dict['artist'] = artist
			context_dict['is_error'] = False
			if request.method == 'POST':
				form = StyleForm(request.POST)
				style = Style.objects.filter(category = form.data['category'], sub_category = form.data['sub_category'])	
				if style:
					style = Style.objects.get(category = form.data['category'], sub_category = form.data['sub_category'])
					ArtistStyle.objects.get_or_create(artist_id = artist, style_id = style)
					return info(request, artist_name_slug)
				else:
					context_dict['is_error'] = True
					context_dict['errors'] = 'There is no such style with this category and sub category'
					form = StyleForm()
					context_dict['form'] = form
					return render(request, 'artist/selectstyle.html', context_dict)
			else:
				form = StyleForm()
			context_dict['form'] = form
			return render(request, 'artist/selectstyle.html', context_dict)
		else:
			return HttpResponse("Only the artist could select the style.")
	except ArtistProfile.DoesNotExist:
		pass
	return HttpResponse("No such artist here")
