from django.contrib import admin
from venue.models import Venue

class VenueAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}
	list_display = ['name', 'websit', 'bio', 'capacity', 'address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country']

# Register your models here.
admin.site.register(Venue, VenueAdmin)
