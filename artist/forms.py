from django import forms
from artist.models import ArtistProfile
from django.contrib.auth.models import User
from concert.models import Concert
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget
from venue.models import Venue

class ArtistProfileForm(forms.ModelForm):
	artname = forms.CharField(widget = forms.HiddenInput(), required = False)
	slug = forms.SlugField(widget = forms.HiddenInput(), required = False)
	websit = forms.URLField(help_text = 'website', required = False)
	bio = forms.CharField(widget = forms.Textarea, required = False, help_text = 'bio')
	picture = forms.ImageField(required = False, help_text = 'picture')
	
	class Meta:
		model = ArtistProfile
		fields = ('websit', 'bio', 'picture', 'slug', 'artname')
		exclude = ('artist', )

class ConcertForm(forms.ModelForm):
	venue = forms.ModelChoiceField(queryset = Venue.objects.all(), help_text = "address")
	ticket_price = forms.IntegerField(help_text = "ticket price")
	ticked_hyperlink = forms.URLField(help_text = "Office ticket website")
	begin_date = forms.DateField(widget = SelectDateWidget, help_text = "concert date")
	begin_time = forms.TimeField(help_text = "begin time")
	end_time = forms.TimeField(help_text = "end time")
	post_time = forms.DateTimeField(widget = forms.HiddenInput(), required = False)
	name = forms.CharField(max_length = 30, help_text = "concert name") 
	remark_state = forms.IntegerField(widget = forms.HiddenInput(), required = False)
	description = forms.CharField(widget = forms.Textarea, required = False, help_text = 'description')

	class Meta:
		model = Concert
		fields = ('name', 'venue', 'begin_date', 'begin_time', 'end_time', 'ticket_price', 'ticked_hyperlink', 'post_time', 'remark_state', 'description')
		exclude = ('artist_id', )

class MissingConcertForm(forms.ModelForm):
	artist_id = forms.ModelChoiceField(queryset = ArtistProfile.objects.all(), help_text = 'artist name')
	venue = forms.ModelChoiceField(queryset = Venue.objects.all(), help_text = "address")
	ticket_price = forms.IntegerField(help_text = "ticket price")
	ticked_hyperlink = forms.URLField(help_text = "Office ticket website")
	begin_date = forms.DateField(widget = SelectDateWidget, help_text = "concert date")
	begin_time = forms.TimeField(help_text = "begin time")
	end_time = forms.TimeField(help_text = "end time")
	post_time = forms.DateTimeField(widget = forms.HiddenInput(), required = False)
	name = forms.CharField(max_length = 30, help_text = "concert name") 
	remark_state = forms.IntegerField(widget = forms.HiddenInput(), required = False)

	class Meta:
		model = Concert
		fields = ('artist_id', 'name', 'venue', 'begin_date', 'begin_time', 'end_time', 'ticket_price', 'ticked_hyperlink', 'post_time', 'remark_state')

from artist.models import Fan
class FanForm(forms.ModelForm):
	follow = forms.BooleanField(help_text = "Following")

	class Meta:
		model = Fan
		fields = ('follow', )
 
