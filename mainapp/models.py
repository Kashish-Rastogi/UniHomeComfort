from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms


# Kashish
class CustomUser(AbstractUser):
    '''
        This model contains all the basic information of user and owner.
    '''
    STATE = [
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NS', 'Nova Scotia'),
        ('NT', 'Northwest Territories'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon'),
    ]
    GENDER=[('Female', 'Female'), ('Male', 'Male')]

    country_code = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    mobile_no = models.IntegerField(validators=[MinValueValidator(1_000_000_000), MaxValueValidator(9_999_999_999)])
    age = models.IntegerField()
    address = models.CharField(max_length=150)
    state = models.CharField(max_length=130, choices=STATE, default='AB')
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=7, choices=GENDER, default='Female')
    identification = models.FileField(upload_to='documents/user/identifications/', null=True, blank=True)
    rental_license = models.FileField(upload_to='documents/user/rental_license/', null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    # Specify unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_permissions')

    def str(self):
        return str(self.first_name)


class Institute(models.Model):
    '''
        This model contains if the user is in univeristy or college
    '''
    INSTITUTE_TYPE = [
        (0, "University"),
        (1, "College")
    ]
    name = models.TextField()
    type = models.IntegerField(default=0, choices=INSTITUTE_TYPE)
    address = models.TextField()


class StudentUser(CustomUser):
    '''
        This model contains all the information of student and inherit properties of user
    '''

    offer_letter = models.FileField(upload_to='documents/offer_letters/')
    country = models.CharField(max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

    def str(self):
        return f"Student Profile - {self.institute}"


class OwnerUser(CustomUser):
    '''
        This model contains all the information of owner and inherit properties of user
    '''
    OCCUPATION_TYPES = [
        (0, "Employed"),
        (1, "Business"),
        (2, "Unemployed"),
    ]

    # identification = models.FileField(upload_to='documents/owner/identifications/')
    # occupation = models.IntegerField(default=0, choices=OCCUPATION_TYPES)

    def str(self):
        return f"Property Owner Profile - {self.first_name}"

# Jainam
class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
    ]
    AVAILABILITY_STATUS = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
        ('coming_soon', 'Coming Soon'),
    ]

    title = models.CharField(max_length=255)
    address = models.TextField()
    city = models.TextField(max_length=50, default='Windsor')
    zipcode = models.TextField(max_length=50, default='N9B 2T6')

    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    amenities = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.CharField(max_length=50, choices=AVAILABILITY_STATUS)
    available_from = models.DateTimeField(default=timezone.now)
    available_to = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    is_biddable = models.BooleanField(default=True)
    bidding_min_limit = models.DecimalField(max_digits=10, decimal_places=2)
    lease_required = models.BooleanField(default=True)
    lease_duration = models.IntegerField(default=12)  # in month
    allowed_lease_people = models.IntegerField(null=False, default=2)
    rules = models.TextField(blank=True)
    owner = models.ForeignKey(OwnerUser, on_delete=models.CASCADE, related_name='owner_name', default=1)
    prop_image1 = models.FileField(upload_to='documents/property_images/', null=True, blank=True)
    prop_image2 = models.FileField(upload_to='documents/property_images/', null=True, blank=True)
    prop_image3 = models.FileField(upload_to='documents/property_images/', null=True, blank=True)
    prop_image4 = models.FileField(upload_to='documents/property_images/', null=True, blank=True)
    prop_image5 = models.FileField(upload_to='documents/property_images/', null=True, blank=True)
    house_build_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


# Tanvi:
class Bidding(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    bidding_status = models.CharField(max_length=100,
                                      choices=[('pending', 'Pending'), ('accepted', 'Accepted'),
                                               ('rejected', 'Rejected')])
    payment_status = models.CharField(max_length=50,
                                      choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])
    bidding_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.property.title

    # def make_payment(self):
    # Integrate with a payment gateway and update is_paid accordingly
    # For example, if using Stripe:
    # stripe_response = stripe.PaymentIntent.create(
    #     amount=int(self.bid_amount * 100),  # Convert to cents
    #     currency='usd',  # Change to your currency
    #     payment_method='pm_card_visa',  # Replace with the actual payment method
    #     confirmation_method='manual',
    # )
    # if stripe_response.status == 'succeeded':
    #     self.is_paid = True
    #     self.save()


class Meta:
    ordering = ['-timestamp']


class Forum(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class PropertyDocument(models.Model):
    DOCUMENT_TYPES = (
        ('title_deed', 'Title Deed'),
        ('lease_agreement', 'Lease Agreement'),
        ('utility_bill', 'Utility Bill'),
        ('building_approval_plan', 'Building Approval Plan'),
        ('occupancy_certificate', 'Occupancy Certificate'),
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




class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name


class CommunityPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



