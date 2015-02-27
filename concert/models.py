from django.db import models
from django.template.defaultfilters import slugify
from venue.models import Venue
from artist.models import ArtistProfile
from django.contrib.auth.models import User

#
# models: Concert, UserLikeConcert, UserRatingConcert, ConcertReviews, UserBuyTickets
#

# Create your models here.
class Concert(models.Model):
	artist_id = models.ForeignKey(ArtistProfile)
	venue = models.ForeignKey(Venue, to_field = "name")
	ticket_price = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
	ticket_hyperlink = models.URLField(null = True)
	begin_date = models.DateField()
	begin_time = models.TimeField()
	end_time = models.TimeField()
	post_time = models.DateTimeField()
	name = models.CharField(max_length = 30)
	remark_state = models.IntegerField(max_length = 1, default = 1)
	description = models.TextField(null = True, blank = True)
		
	def __unicode__(self):
		return self.name
	
	class Meta:
		unique_together = (('artist_id', 'begin_date', 'begin_time'))

from member.models import UserProfile, UserReviews

class UserLikeConcert(models.Model):
	user_id = models.ForeignKey(User)
	concert_id = models.ForeignKey(Concert)
	time = models.DateTimeField()

	class Meta:
		unique_together = (('user_id', 'concert_id'))

class UserRatingConcert(models.Model):
	user_id = models.ForeignKey(User)
	concert_id = models.ForeignKey(Concert)
	time = models.DateTimeField()
	rating = models.DecimalField(max_digits = 3, decimal_places = 1)
	
	class Meta:
		unique_together = (('user_id', 'concert_id'))

class ConcertReviews(models.Model):
	concert_id = models.ForeignKey(Concert)
	review_id = models.ForeignKey(UserReviews)
	
	class Meta:
		unique_together = (('concert_id', 'review_id'))
	
class UserBuyTickets(models.Model):
	user_id = models.ForeignKey(User)
	concert_id = models.ForeignKey(Concert)
	time = models.DateTimeField()
	numbers = models.IntegerField(max_length = 2)

