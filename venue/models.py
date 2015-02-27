from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Venue(models.Model):
	name = models.CharField(max_length = 30, unique = True)
	slug = models.SlugField(unique = True)
	websit = models.URLField(blank = True)
	bio = models.TextField(null = True)
	address_line1 = models.CharField("Address line 1", max_length = 45, null = True, blank = True)		
	address_line2 = models.CharField("Address line 2", max_length = 45, null = True, blank = True)
	postal_code = models.CharField("Postal Code", max_length = 10, null = True, blank = True)
	city = models.CharField(max_length = 50, null = True, blank = True)
	state_province = models.CharField("State/Province", max_length = 40, blank = True, null = True)
	country = models.CharField(max_length = 45, blank = True, null = True)
	capacity = models.IntegerField(max_length = 4)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Venue, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name
