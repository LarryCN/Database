from django.contrib import admin
from member.models import UserProfile, Style, UserStyle, UserFollowUser ,UserReviews, UserRecommendation, RecommendationReviews, RecommendationConcerts, MissingConcert 
from member.models import Category, SubCategory

#class UserProfileAdmin(admin.ModelAdmin):
#	list_display = ['birthday', 'gender', 'credits', 'picture']

class StyleAdmin(admin.ModelAdmin):
	list_display = ['category', 'sub_category']

class UserStyleAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'style_id']

class UserReviewsAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'time', 'review']

class UserRecommendationAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'time', 'name']

class RecommendationReviewsAdmin(admin.ModelAdmin):
	list_display = ['recommendation_id', 'review_id']

class RecommendationConcertsAdmin(admin.ModelAdmin):
	list_display = ['recommendation_id', 'concert_id']

class MissingConcertAdmin(admin.ModelAdmin):
	list_display = ['concert', 'user_id']

class UserFollowUserAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'follower_id']

# Register your models here.
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserFollowUser, UserFollowUserAdmin)
admin.site.register(UserStyle, UserStyleAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(UserReviews, UserReviewsAdmin)
admin.site.register(UserRecommendation, UserRecommendationAdmin)
admin.site.register(RecommendationReviews, RecommendationReviewsAdmin)
admin.site.register(RecommendationConcerts, RecommendationConcertsAdmin)
admin.site.register(MissingConcert, MissingConcertAdmin)
