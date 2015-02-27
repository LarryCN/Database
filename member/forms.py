from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from member.models import Style, UserProfile, UserReviews, UserRecommendation, RecommendationConcerts, UserFollowUser, Category, SubCategory
from concert.models import Concert
from venue.models import Venue
from artist.models import ArtistProfile

class SearchForm(forms.ModelForm):
	keyword = forms.CharField(max_length = 50, required = False, help_text = 'key words(less than 50)')
	city = forms.ModelChoiceField(queryset = Venue.objects.distinct('city').values_list('city'), required = False, help_text = 'City')

	class Meta:
		pass

class UserFollowUserForm(forms.ModelForm):
	follow = forms.BooleanField(help_text = "Following")

	class Meta:
		model = UserFollowUser
		fields = ('follow', )

class RecommendationConcertsForm(forms.ModelForm):
	concert_id = forms.ModelChoiceField(queryset = Concert.objects.all(), help_text = 'Select a concert')
	
	class Meta:
		model = RecommendationConcerts
		fields = ('concert_id', )

class StyleForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset = Category.objects.all(), help_text = "category")
	sub_category = forms.ModelChoiceField(queryset = SubCategory.objects.all(), help_text = "sub category")

	class Meta:
		model = Style
		fields = ('category', 'sub_category')

class UserProfileForm(forms.ModelForm):	
	name = forms.CharField(widget = forms.HiddenInput(), required = False)
	slug = forms.SlugField(widget = forms.HiddenInput(), required = False)
	birthday = forms.DateField(widget = SelectDateWidget(years=range(1900, 2100)), required = False, help_text = "birthday" )
	credits = forms.IntegerField(widget = forms.HiddenInput(), required = False)
	address_line1 = forms.CharField(max_length = 45, required = False, help_text = 'address line1')
	address_line2 = forms.CharField(max_length = 45, required = False, help_text = 'address line2')
	postal_code = forms.CharField(max_length = 10, required = False, help_text = 'postal code')
	city = forms.CharField(max_length = 50, required = False, help_text = 'city')
	state_province = forms.CharField(help_text = "State/Province", max_length = 40, required = False)
	country = forms.CharField(max_length = 45, required = False, help_text = 'country')
	picture = forms.ImageField(required = False)

	class Meta:
		model = UserProfile
		fields = ('name', 'slug', 'birthday', 'credits', 'address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country', 'picture')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class UserReviewsForm(forms.ModelForm):
	review = forms.CharField(widget = forms.Textarea, required = False, help_text = 'review')

	class Meta:
		model = UserReviews
		fields = ('review', )

class UserRecommendationForm(forms.ModelForm):
	name = forms.CharField(max_length = 30, help_text = 'recommendation name')

	class Meta:
		model = UserRecommendation
		fields = ('name', )
	

