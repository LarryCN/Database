from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from concert.models import Concert, UserLikeConcert, UserRatingConcert, ConcertReviews, UserBuyTickets
from member.forms import UserReviewsForm
from member.models import UserReviews
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from artist.models import ArtistProfile
from venue.models import Venue
from concert.forms import UserRatingConcertForm, UserLikeConcertForm, UserBuyTicketsForm
from django.db.models import Avg, Sum

POST_BY_ARTIST = 1
POST_BY_USER_UNCONFIRM = 2
POST_BY_USER_CONFIRM = 3
POST_BY_USER_FAKE = 4
POST_BY_ADMIN = 5

# Create your views here.
@login_required
def ticket(request, concert_id):
	try:
		context_dict = {}
		concert = Concert.objects.get(pk = concert_id)
		capacity = Concert.objects.filter(pk = concert_id).select_related('venue')[0].venue.capacity
		bought = UserBuyTickets.objects.filter(concert_id = concert).aggregate(Sum('numbers')).values()[0]
		if not bought:
			bought = 0
		left = capacity - bought
		print(bought, left)
		context_dict['errors'] = ''
		have_buy = UserBuyTickets.objects.filter(concert_id = concert, user_id = request.user).aggregate(Sum('numbers')).values()[0]
		if not have_buy:
			have_buy = 0	
		if have_buy >= 10:
			context_dict['errors'] = 'Each user could buy max 10 tickets'
		context_dict['have_buy'] = have_buy
		context_dict['ten'] = False
		if have_buy >= 10:	
			context_dict['ten'] = True
		if request.method == 'POST' and not context_dict['errors']:
			form = UserBuyTicketsForm(request.POST)
	
			if form.is_valid():
				ticket = form.save(commit = False)
				if left >= ticket.numbers and ticket.numbers <= (10 - have_buy):
					ticket.time = timezone.now()
					ticket.user_id = request.user
					ticket.concert_id = concert
					ticket.save()
					return info(request, concert_id)
				else:
					if left < form.numbers:
						context_dict['errors'] = 'Not enough tickets to sell'
					else:
						context_dict['errors'] = 'Each user could buy max 10 tickets'	
					form = UserBuyTicketsForm()
			else:
				print form.errors
		else:
			form = UserBuyTicketsForm()
		context_dict['form'] = form
		context_dict['concert'] = concert
		return render(request, 'concert/ticket.html', context_dict)
	except Concert.DoesNotExist:
		pass
	return HttpResponse("No such concert here")

@login_required
def like(request, concert_id):
	try:
		context_dict = {}
		concert = Concert.objects.get(pk = concert_id)
		likes = UserLikeConcert.objects.filter(concert_id = concert)
		context_dict['likes'] = likes
		context_dict['is_like'] = False
		user = UserLikeConcert.objects.filter(concert_id = concert, user_id = request.user)
		if user:
			context_dict['is_like'] = True
		if request.method == 'POST':
			form = UserLikeConcertForm(request.POST)
	
			if form.is_valid():
				like = form.save(commit = False)
				like.time = timezone.now()
				like.user_id = request.user
				like.concert_id = concert
				like.save()
				return info(request, concert_id)
			else:
				print form.errors
		else:
			form = UserLikeConcertForm()
		context_dict['form'] = form
		context_dict['concert'] = concert
		return render(request, 'concert/like.html', context_dict)
	except Concert.DoesNotExist:
		pass
	return HttpResponse("No such concert here")

@login_required
def ratingdetail(request, concert_id):
	try:
		context_dict = {}
		concert = Concert.objects.get(pk = concert_id)
		ratings = UserRatingConcert.objects.filter(concert_id = concert)
		context_dict['ratings'] = ratings
		context_dict['have_rating'] = False
		user = UserRatingConcert.objects.filter(concert_id = concert, user_id = request.user)
		if user:
			context_dict['have_rating'] = True
		if request.method == 'POST':
			form = UserRatingConcertForm(request.POST)
	
			if form.is_valid():
				rating = form.save(commit = False)
				rating.time = timezone.now()
				rating.user_id = request.user
				rating.concert_id = concert
				rating.save()
				return info(request, concert_id)
			else:
				print form.errors
		else:
			form = UserRatingConcertForm()
		context_dict['form'] = form
		context_dict['concert'] = concert
		return render(request, 'concert/ratingdetail.html', context_dict)
	except Concert.DoesNotExist:
		pass
	return HttpResponse("No such concert here")
	

def index(request):
	concert_list = Concert.objects.all()[:]
	context_dict = {'concerts': concert_list}

	response = render(request, 'concert/index.html', context_dict)

	return response

def info(request, concert_id):	
	context_dict = {}
	try:
		concert = Concert.objects.get(pk = concert_id)
		capacity = Concert.objects.filter(pk = concert_id).select_related('venue')[0].venue.capacity
		bought = UserBuyTickets.objects.filter(concert_id = concert).aggregate(Sum('numbers')).values()[0]
		if not bought:
			bought = 0
		left = capacity - bought
		reviews = ConcertReviews.objects.filter(concert_id = concert_id).select_related('review_id')
		artist = ArtistProfile.objects.get(artname = concert.artist_id)
		venue = Venue.objects.get(name = concert.venue)
		avg_rating = UserRatingConcert.objects.filter(concert_id = concert).aggregate(Avg('rating')).values()[0]
		count = UserLikeConcert.objects.filter(concert_id = concert).count()
		context_dict['concert'] = concert	
		context_dict['reviews'] = reviews
		context_dict['artist'] = artist
		context_dict['venue'] = venue
		context_dict['avg_r'] = avg_rating
		context_dict['count'] = count
		context_dict['left'] = left
	except Concert.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything - the template displays the "no category" message for us.
		pass

	return render(request, 'concert/info.html', context_dict)

@login_required
def reviews(request, concert_id):
	try:
		context_dict = {}
		concert = Concert.objects.get(pk = concert_id)
		if request.method == 'POST':
			form = UserReviewsForm(request.POST)
	
			if form.is_valid():
				review = form.save(commit = False)
				review.time = timezone.now()
				review.user_id = request.user
				review.save()
				ConcertReviews.objects.get_or_create(concert_id = concert, review_id = review)
				return info(request, concert_id)
			else:
				print form.errors
		else:
			form = UserReviewsForm()
		context_dict['form'] = form
		context_dict['concert'] = concert
		return render(request, 'concert/reviews.html', context_dict)
	except Concert.DoesNotExist:
		pass
	return HttpResponse("No such concert here")
