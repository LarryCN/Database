from django.contrib import admin
from artist.models import ArtistProfile, ArtistStyle, Fan

class ArtistProfileAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('artname', )}
	list_display = ['artname', 'websit', 'bio', 'picture']

class ArtistStyleAdmin(admin.ModelAdmin):
	list_display = ['artist_id', 'style_id']

class FanAdmin(admin.ModelAdmin):
	list_display = ['artist_id', 'user_id']

# Register your models here.
admin.site.register(ArtistProfile, ArtistProfileAdmin)
admin.site.register(ArtistStyle, ArtistStyleAdmin)
admin.site.register(Fan, FanAdmin)
