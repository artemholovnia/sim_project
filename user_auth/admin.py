from django.contrib import admin
from django.contrib.auth.models import User as U
from .models import UserProfileImage, UserProfile
from django.contrib.sessions.models import Session

# Register your models here.

class UserProfileImageStackedInline(admin.StackedInline):
    model = UserProfileImage
    fields = ['image']
    extra = 1

class UserProfileStackedInline(admin.StackedInline):
    model = UserProfile
    fields = ['flags']

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileImageStackedInline, UserProfileStackedInline]

admin.site.unregister(U)
admin.site.register(U, UserAdmin)

admin.site.register(UserProfile)
admin.site.register(Session)