from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from member.models import UserProfile, Style, UserStyle, UserFollowUser ,UserReviews, UserRecommendation, RecommendationReviews, RecommendationConcerts, MissingConcert 
from member.forms import UserProfileForm, UserForm, UserRecommendationForm, RecommendationConcertsForm, UserFollowUserForm, UserReviewsForm, StyleForm
from django.utils import timezone
from artist.models import ArtistProfile, Fan
from django.contrib.auth.models import User
from member.models import Category, SubCategory
from artist.forms import ConcertForm, MissingConcertForm
from concert.views import POST_BY_USER_UNCONFIRM, POST_BY_USER_CONFIRM, POST_BY_USER_FAKE
from concert.models import Concert, UserBuyTickets
from django.db.models import Q

def index(request):
	if request.user:
		context_dict = {}
		context_dict['newposts'] = Concert.objects.filter(Q(remark_state = 1) | Q(remark_state = 3) | Q(remark_state = 5)).order_by('-post_time')[:3]
		tmp = Concert.objects.raw("select id, name from concert_concert natural join member_recommendationconcerts")
		for t in tmp:
			print(t)
		if request.method == "GET":
			tmp = request.GET.get('key', False)
			context_dict['results'] = Concert.objects.filter(description__contains = tmp)
		return render(request, 'member/index.html', context_dict)
	else:
		return render(request, 'member/index.html', {})

@login_required
def missingconcert(request, user_name_slug):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		context_dict = {}
		if request.user == member.user:
			context_dict['member'] = member
			context_dict['is_error'] = False
			if request.method == 'POST':
				form = MissingConcertForm(request.POST)
	
				if form.is_valid():
					concert = form.save(commit = False)
					concert.post_time = timezone.now()
					concert.remark_state = POST_BY_USER_UNCONFIRM
					concert.save()
					postconcert = Concert.objects.get(artist_id = concert.artist_id, begin_time = concert.begin_time, begin_date = concert.begin_date)
					MissingConcert.objects.get_or_create(user_id = member, concert = postconcert)
					return homepage(request, user_name_slug)
				else:
					context_dict['is_error'] = True
					context_dict['errors'] = form.errors
			else:
				form = MissingConcertForm()
			context_dict['form'] = form
			return render(request, 'member/missingconcert.html', context_dict)
		else:
			return HttpResponse("Only the user could post a new concert.")
	except UserProfile.DoesNotExist:
		pass
	return HttpResponse("No such user here")

@login_required
def selectstyle(request, user_name_slug):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		if request.user == member.user:
			context_dict = {}
			context_dict['member'] = member
			context_dict['is_error'] = False
			if request.method == 'POST':
				form = StyleForm(request.POST)
				style = Style.objects.filter(category = form.data['category'], sub_category = form.data['sub_category'])	
				if style:
					style = Style.objects.get(category = form.data['category'], sub_category = form.data['sub_category'])
					UserStyle.objects.get_or_create(user_id = member, style_id = style)
					return homepage(request, user_name_slug)
				else:
					context_dict['is_error'] = True
					context_dict['errors'] = 'There is no such style with this category and sub category'
					form = StyleForm()
					context_dict['form'] = form
					return render(request, 'member/selectstyle.html', context_dict)
			else:
				form = StyleForm()
			context_dict['form'] = form
			return render(request, 'member/selectstyle.html', context_dict)
		else:
			return HttpResponse("Only the user could select the style.")
	except UserProfile.DoesNotExist:
		pass
	return HttpResponse("No such user here")

@login_required
def add_review(request, user_name_slug, recommendation_id):
	try:
		context_dict = {}
		member = UserProfile.objects.get(slug = user_name_slug)
		recommendation = UserRecommendation.objects.get(pk = recommendation_id)
		if request.method == 'POST':
			form = UserReviewsForm(request.POST)
	
			if form.is_valid():
				review = form.save(commit = False)
				review.time = timezone.now()
				review.user_id = request.user
				review.save()
				RecommendationReviews.objects.get_or_create(recommendation_id = recommendation, review_id = review)
				return recommendationdetail(request, user_name_slug, recommendation_id)
			else:
				print form.errors
		else:
			form = UserReviewsForm()
		context_dict['member'] = member
		context_dict['form'] = form
		context_dict['recommendation'] = recommendation
		return render(request, 'member/reviews.html', context_dict)
	except UserProfile.DoesNotExist or UserRecommendation.DoesNotExist:
		pass
	return HttpResponse("Take the wrong place")

@login_required
def follower(request, user_name_slug):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		context_dict = {}
		context_dict['member'] = member
		fans = UserFollowUser.objects.filter(user_id = member).select_related('follower_id')
		context_dict['fans'] = fans
		return render(request, 'member/follower.html', context_dict)
	except ArtistProfile.DoesNotExist:
		pass
	return HttpResponse("No such user here")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/member/')

@login_required
def home(request):
	userobj = User.objects.get(username = request.user)
	artist = ArtistProfile.objects.filter(artist = userobj)
	if artist:
		artist = ArtistProfile.objects.get(artist = userobj)
		return HttpResponseRedirect('/artist/' + artist.slug)
	user = UserProfile.objects.filter(user = userobj)
	if user:
		user = UserProfile.objects.get(user = userobj)
		return homepage(request, user.slug)
	return HttpResponseRedirect('/admin/')

def restricted(request):
	info = 'Since you`re logged in, you can see this text'
	return render(request, 'member/restricted.html', {'info': info})

def homepage(request, user_name_slug):
	context_dict = {}
	try:
		user = UserProfile.objects.get(slug = user_name_slug)
		context_dict['member'] = user
		context_dict['can_rd'] = False
		rd = UserRecommendation.objects.filter(user_id = user)
		context_dict['recommendation'] = rd
		member = UserProfile.objects.filter(user = request.user)
		fans = UserFollowUser.objects.filter(user_id = user).count()
		context_dict['fans'] = fans
		context_dict['is_user'] = False
		context_dict['user_self'] = False
		style = UserStyle.objects.all().select_related('style_id')
		is_null = SubCategory.objects.get(name = 'null')
		context_dict['missingconcerts'] = MissingConcert.objects.filter(user_id = user).select_related('concert')
		styles = ''
		for s in style:
			if s.style_id.sub_category == is_null:
				styles += str(s.style_id.category.name) + '   '
			else:
				styles += (str(s.style_id.category.name) + '-' + str(s.style_id.sub_category.name)) + ' '
		context_dict['styles'] = styles
		context_dict['can_p'] = False
		context_dict['concerns'] = Fan.objects.filter(user_id = user).select_related('artist_id')
		if user.user == request.user:
			context_dict['user_self'] = True
			if user.credits > 50:
				context_dict['can_rd'] = True			
			if user.credits > 100:
				context_dict['can_p'] = True
			context_dict['goconcerts'] = UserBuyTickets.objects.filter(user_id = user.user).distinct('concert_id').select_related('concert_id')
		if member:
			context_dict['is_user'] = True
			context_dict['is_fan'] = False
			member = UserProfile.objects.get(user = request.user)
			fan = UserFollowUser.objects.filter(user_id = user, follower_id = member)
			if fan:
				context_dict['is_fan'] = True
			if member == user:
				context_dict['is_user'] = False
				context_dict['is_fan'] = True
			if request.method == 'POST' and not context_dict['is_fan']:
				form = UserFollowUserForm(request.POST)
				
				if form.is_valid():
					follow = form.save(commit = False)
					tmp = UserFollowUser()
					tmp.time = timezone.now()
					tmp.user_id = user
					tmp.follower_id = member
					tmp.save()
					return homepage(request, user_name_slug)
			else:
				form = UserFollowUserForm()
			context_dict['form'] = form
	except UserProfile.DoesNotExist:
		# We get here if we didn't find the specified category.
		# Don't do anything - the template displays the "no category" message for us.
		pass
	
	return render(request, 'member/homepage.html', context_dict)

def about(request):
	# If the visits session varible exists, take it and use it.
	# If it doesn't, we haven't visited the site so set the count to zero.
	return render(request, 'member/about.html', {})

def recommendationdetail(request, user_name_slug, recommendation_id):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		rd = UserRecommendation.objects.get(pk = recommendation_id)
		concert = RecommendationConcerts.objects.filter(recommendation_id = rd).select_related('concert_id')
		reviews = RecommendationReviews.objects.filter(recommendation_id = recommendation_id).select_related('review_id')
		context_dict = {}
		context_dict['member'] = member
		context_dict['recommendation'] = rd
		context_dict['concerts'] = concert
		context_dict['reviews'] = reviews
		context_dict['add_concert'] = False
		if request.user == member.user:
			context_dict['add_concert'] = True			
		return render(request, 'member/recommendationdetail.html', context_dict)
	except UserProfile.DoesNotExist or UserRecommendation.DoesNotExist:
		pass
	return HttpResponse("No such user here")

def add_concert(request, user_name_slug, recommendation_id):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		rd = UserRecommendation.objects.get(pk = recommendation_id)
		context_dict = {}
		context_dict['user'] = member
		context_dict['recommendation'] = rd
		if request.user == member.user:
			if request.method == 'POST':
				form = RecommendationConcertsForm(request.POST)
	
				if form.is_valid():
					recommendation = form.save(commit = False)
					recommendation.recommendation_id = rd
					tmp = RecommendationConcerts.objects.filter(recommendation_id = rd, concert_id = recommendation.concert_id)
					if tmp:
						return HttpResponse('You have add this concert')
					recommendation.save()
					
					return recommendationdetail(request, user_name_slug, recommendation_id)
				else:
					print form.errors
			else:
				form = RecommendationConcertsForm()
			context_dict['form'] = form
			return render(request, 'member/add_concert.html', context_dict)
		else:
			return HttpResponse("only the user coulde add a concert") 
	except UserProfile.DoesNotExist or UserRecommendation.DoesNotExist:
		pass
	return HttpResponse("No such user here")

def recommendation(request, user_name_slug):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		if request.user == member.user:
			context_dict = {}
			context_dict['user'] = member
			if request.method == 'POST':
				form = UserRecommendationForm(request.POST)
	
				if form.is_valid():
					user = form.save(commit = False)
					user.user_id = member
					user.time = timezone.now()
					tmp = UserRecommendation.objects.filter(user_id = member, name = user.name)
					if tmp:
						return HttpResponse('You have created a recommendation with this name')
					user.save()
					
					return homepage(request, user_name_slug)
				else:
					print form.errors
			else:
				form = UserRecommendationForm()
			context_dict['form'] = form
			return render(request, 'member/recommendation.html', context_dict)
		else:
			return HttpResponse("Only the user could edit the information.")
	except UserProfile.DoesNotExist:
		pass
	return HttpResponse("No such user here")

def edit(request, user_name_slug):
	try:
		member = UserProfile.objects.get(slug = user_name_slug)
		if request.user == member.user:
			context_dict = {}
			context_dict['user'] = member
			if request.method == 'POST':
				userform = UserForm(request.POST)
				form = UserProfileForm(request.POST, request.FILES)
	
				if form.is_valid() and userform.is_valid():
					user = form.save(commit = False)
					userf = userform.save(commit = False)
					member.address_line1 = user.address_line1
					member.address_line2 = user.address_line2
					member.city = user.city
					member.postal_code = user.postal_code
					member.state_province = user.state_province
					member.country = user.country
					member.picture = user.picture
					member.birthday = user.birthday
					request.user.first_name = userf.first_name
					request.user.last_name = userf.last_name
					request.user.email = userf.email
					member.save()
					request.user.save()
					return homepage(request, user_name_slug)
				else:
					print form.errors
			else:
				form = UserProfileForm()
				userform = UserForm()
			context_dict['form'] = form
			context_dict['userform'] = userform
			return render(request, 'member/edit.html', context_dict)
		else:
			return HttpResponse("Only the user could edit the information.")
	except UserProfile.DoesNotExist:
		pass
	return HttpResponse("No such user here")
