from django.contrib import admin
from .models import AppUser, Institute, Property, Bidding, Forum, PropertyDocument, Category, PropertyType, \
    CommunityPost, PropertyVisits, City


def user_type(obj):
    if obj.is_owner:
        return "Owner"
    else:
        return "Student"

class AppUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', user_type]

class BiddingAdmin(admin.ModelAdmin):
    list_display = ['id', 'property', 'student', 'bidding_amount']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'zipcode']


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Institute)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Forum)
admin.site.register(PropertyDocument)
admin.site.register(Category)
admin.site.register(CommunityPost)
admin.site.register(PropertyVisits)
admin.site.register(City)

