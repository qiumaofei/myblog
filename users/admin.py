from django.contrib import admin

# Register your models here.
from users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
	#
	list_display = ('id', 'username', 'phone', 'email', 'first_name', 'last_name')
	list_per_page = 5
	list_editable = ['email', 'first_name', 'last_name']
	list_display_links = ('username', 'phone')
	list_filter = ('username', 'phone')
	search_fields = ('phone', 'username')


admin.site.register(UserProfile, UserProfileAdmin)
