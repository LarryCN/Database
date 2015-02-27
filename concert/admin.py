from django.contrib import admin
from concert.models import Concert, UserLikeConcert, UserRatingConcert, ConcertReviews, UserBuyTickets


class UserLikeConcertAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'concert_id', 'time']

class UserRatingConcertAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'concert_id', 'time', 'rating']

class ConcertReviewsAdmin(admin.ModelAdmin):
	list_display = ['concert_id', 'review_id']

class UserBuyTicketsAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'concert_id', 'time', 'numbers']

# Register your models here.
admin.site.register(Concert)
admin.site.register(UserLikeConcert, UserLikeConcertAdmin)
admin.site.register(UserRatingConcert, UserRatingConcertAdmin)
admin.site.register(ConcertReviews, ConcertReviewsAdmin)
admin.site.register(UserBuyTickets, UserBuyTicketsAdmin)
