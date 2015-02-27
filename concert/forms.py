from django import forms
from django.contrib.auth.models import User
from member.models import Style, UserProfile, UserReviews, UserRecommendation, RecommendationConcerts
from concert.models import Concert, UserRatingConcert, UserLikeConcert, UserBuyTickets

class UserRatingConcertForm(forms.ModelForm):
	rating = forms.DecimalField(max_digits = 3, decimal_places = 1, max_value = 10.0, min_value = 0.0, help_text = 'Give A Rating (0.0 ~ 10.0)')
	
	class Meta:
		model = UserRatingConcert
		fields = ('rating', )
	
class UserLikeConcertForm(forms.ModelForm):
	like = forms.BooleanField(help_text = 'Do you want to go to the concert?')
	
	class Meta:
		model = UserLikeConcert
		fields = ('like', )

class UserBuyTicketsForm(forms.ModelForm):
	numbers = forms.IntegerField(help_text = 'Choose how many tickets you want to buy?')
	
	class Meta:
		model = UserBuyTickets
		fields = ('numbers', )
