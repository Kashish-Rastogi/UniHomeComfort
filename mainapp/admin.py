from django.contrib import admin
from .models import AppUser, Institute, Property, Bidding, Forum, PropertyDocument, Category, PropertyType


def user_type(obj):
    if obj.is_owner:
        return "Owner"
    else:
        return "Student"

class AppUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', user_type]

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Institute)
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(Bidding)
admin.site.register(Forum)
admin.site.register(PropertyDocument)
admin.site.register(Category)
