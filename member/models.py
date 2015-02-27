from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

#
# models: UserProfiel, Sytle, UserStyle, UserFollowUser, ,UserReviews, UserRecommendation, RecommendationReviews 
#         RecommendationConcerts, MissingConcert
#
class UserProfile(models.Model):
	user = models.OneToOneField(User)

	name = models.CharField(max_length = 30, unique = True)
	slug = models.SlugField(unique = True)
	birthday = models.DateField(null = True)
	credits = models.IntegerField(default = 0)
	address_line1 = models.CharField("Address line 1", max_length = 45, null = True, blank = True)
	address_line2 = models.CharField("Address line 2", max_length = 45, null = True, blank = True)
	postal_code = models.CharField("Postal Code", max_length = 10, null = True, blank = True)
	city = models.CharField(max_length = 50, null = True, blank = True)
	state_province = models.CharField("State/Province", max_length = 40, blank = True, null = True)
	country = models.CharField(max_length = 45, blank = True, null = True)
	picture = models.ImageField(upload_to='member/images', blank = True, null = True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(UserProfile, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.name

class Style(models.Model):
	category = models.ForeignKey(Category)
	sub_category = models.ForeignKey(SubCategory)
	
	class Meta:
		unique_together = (('category', 'sub_category'))

class UserStyle(models.Model):
	user_id = models.ForeignKey(UserProfile)
	style_id = models.ForeignKey(Style)
	
	class Meta:
		unique_together = (('user_id', 'style_id'))

class UserFollowUser(models.Model):
	user_id = models.ForeignKey(UserProfile)
	follower_id = models.ForeignKey(UserProfile, related_name = 'follower_id')
	time = models.DateTimeField()
	
	class Meta:
		unique_together = (('user_id', 'follower_id'))

class UserReviews(models.Model):
	user_id = models.ForeignKey(User)
	time = models.DateTimeField()
	review = models.TextField()
	
	class Meta:
		unique_together = (('user_id', 'time'))

class UserRecommendation(models.Model):
	user_id = models.ForeignKey(UserProfile)
	time = models.DateTimeField()
	name = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = (('user_id', 'name'))

class RecommendationReviews(models.Model):
	recommendation_id = models.ForeignKey(UserRecommendation)
	review_id = models.ForeignKey(UserReviews)

	class Meta:
		unique_together = (('recommendation_id', 'review_id'))

from concert.models import Concert

class RecommendationConcerts(models.Model):
	recommendation_id = models.ForeignKey(UserRecommendation)
	concert_id = models.ForeignKey(Concert)

	class Meta:
		unique_together = (('recommendation_id', 'concert_id'))

class MissingConcert(models.Model):
	concert = models.OneToOneField(Concert)

	user_id = models.ForeignKey(UserProfile)
	
	class Meta:
		unique_together = (('concert', 'user_id'))

	def __unicode__(self):
		return self.concert.name

