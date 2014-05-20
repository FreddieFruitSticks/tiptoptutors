from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from userprofile.models import UserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ('username', 'first_name', 'last_name',)
    list_per_page = 20

admin.site.register(User, UserProfileAdmin)