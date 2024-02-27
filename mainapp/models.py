from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


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

    country_code = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    mobile_no = models.IntegerField(validators=[MinValueValidator(1_000_000_000), MaxValueValidator(9_999_999_999)])
    age = models.IntegerField()
    address = models.CharField(max_length=150)
    state = models.CharField(max_length=130, choices=STATE, default='AB')
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Specify unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_permissions')

    def str(self):
        return str(self.first_name)


class Institute(models.Model):
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

    identification = models.FileField(upload_to='documents/owner/identifications/')
    occupation = models.IntegerField(default=0, choices=OCCUPATION_TYPES)

    def str(self):
        return f"Property Owner Profile - {self.first_name}"


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