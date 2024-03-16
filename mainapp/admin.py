from django.contrib import admin
from .models import StudentUser, OwnerUser, Institute, Property, Bidding, Forum, PropertyDocument, Category


admin.site.register(StudentUser)
admin.site.register(OwnerUser)
admin.site.register(Institute)
admin.site.register(Property)
admin.site.register(Bidding)
admin.site.register(Forum)
admin.site.register(PropertyDocument)
admin.site.register(Category)
