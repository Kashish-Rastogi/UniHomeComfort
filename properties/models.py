from django.db import models

# Create your models here.
from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
        # Additional property types as needed
    )
    AVAILABILITY_STATUS = (
        ('available', 'Available'),
        ('not_available', 'Not Available'),
        ('coming_soon', 'Coming Soon'),
    )

    title = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    amenities = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=50, choices=AVAILABILITY_STATUS)
    listing_date = models.DateField()
    owner_agency = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.title


class PropertyDocument(models.Model):
    DOCUMENT_TYPES = (
        ('title_deed', 'Title Deed'),
        ('lease_agreement', 'Lease Agreement'),
        ('utility_bill', 'Utility Bill'),
        ('building_approval_plan', 'Building Approval Plan'),
        ('occupancy_certificate', 'Occupancy Certificate'),
        # Add more document types as needed
    )
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_image = models.ImageField(upload_to='documents/')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    description = models.TextField(blank=True)
    verification_status = models.BooleanField(default=False, help_text="True if the document has been verified")
    upload_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.property.id}"