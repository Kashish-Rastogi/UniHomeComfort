from django.contrib import admin
from .models import StudentUser, OwnerUser, Institute, Property

admin.site.register(StudentUser)
admin.site.register(OwnerUser)
admin.site.register(Institute)
admin.site.register(Property)