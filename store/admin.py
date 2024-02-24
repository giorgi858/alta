from django.contrib import admin
from .models import Product, Category, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)


# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# Unregister old user
admin.site.unregister(User)


# Re-Register the new way

admin.site.register(User, UserAdmin)
