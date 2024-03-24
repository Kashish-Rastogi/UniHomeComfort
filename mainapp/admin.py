from django.contrib import admin
<<<<<<< HEAD
from .models import AppUser, Institute, Property, Bidding, Forum, PropertyDocument, Category, PropertyType, CommunityPost
=======
from .models import AppUser, Institute, Property, Bidding, Forum, PropertyDocument, Category, PropertyType, \
    CommunityPost, PropertyVisits, City
>>>>>>> fe365b6db74c95a36d358c9286706a2eaa388b2b


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
<<<<<<< HEAD
=======
admin.site.register(PropertyVisits)
admin.site.register(City)
>>>>>>> fe365b6db74c95a36d358c9286706a2eaa388b2b
