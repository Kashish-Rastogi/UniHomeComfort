from django.contrib import admin
from .models import PropertyDocument, Property  # Import any other models you need

# Define admin classes if needed
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'property', 'upload_date', 'verification_status')
    # any other custom settings

# Register models
admin.site.register(PropertyDocument, PropertyDocumentAdmin)
admin.site.register(Property)
