from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

#
# models: ArtistProfile, ArtistStyle, Fan
#
# Fan: user to artist
#

class ArtistProfile(models.Model):
	artist = models.OneToOneField(User)	

	artname = models.CharField(max_length = 30, unique = True)
	slug = models.SlugField(unique = True)
	websit = models.URLField(blank = True, null = True)
	bio = models.TextField(null = True, blank = True)
	picture = models.ImageField(upload_to='artist/images', blank = True, null = True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.artname)
		super(ArtistProfile, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.artname

from member.models import UserProfile, Style

class ArtistStyle(models.Model):
	artist_id = models.ForeignKey(ArtistProfile)
	style_id = models.ForeignKey(Style)

	class Meta:
		unique_together = (('artist_id', 'style_id'))

class Fan(models.Model):
	artist_id = models.ForeignKey(ArtistProfile)
	user_id = models.ForeignKey(UserProfile)
	time = models.DateTimeField()
	
	class Meta:
		unique_together = (('artist_id', 'user_id'))
