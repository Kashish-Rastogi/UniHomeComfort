from django.contrib import admin
from .models import AppUser, Institute, Property, Bidding, Forum, PropertyDocument, Category, CommunityPost


admin.site.register(AppUser)
admin.site.register(Institute)
admin.site.register(Property)
admin.site.register(Bidding)
admin.site.register(Forum)
admin.site.register(PropertyDocument)
admin.site.register(Category)
admin.site.register(CommunityPost)
