from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin, Group, Permission
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, Group, Permission, BaseUserManager
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

# def InstitutionChoices():
#     universities = [
#         ("UOW", "University of Windsor"),
#         ("UBC", "University of British Columbia"),
#         ("SFU", "Simon Fraser University"),
#         ("UCalgary", "University of Calgary"),
#         ("UV", "University of Victoria"),
#         ("UofT", "University of Toronto"),
#         ("UW", "University of Waterloo"),
#         ("UA", "University of Alberta"),
#         ("Q", "Queen’s University"),
#         ("UofM", "University of Manitoba"),
#         ("UQAM", "Université du Québec à Montréal"),
#         ("UofS", "University of Saskatchewan"),
#         ("UofN", "University of New Brunswick"),
#         ("UdeS", "Université de Sherbrooke"),
#         ("WLU", "Wilfrid Laurier University"),
#         ("UofR", "University of Regina"),
#         ("EPMT", "École Polytechnique de Montréal"),
#         ("UofL", "University of Lethbridge"),
#         ("UofW", "The University of Winnipeg"),
#         ("UQ", "Université de Montréal"),
#         ("UofH", "McMaster University"),
#         ("TU", "Toronto Metropolitan University"),
#         ("UO", "University of Ottawa"),
#         ("UofG", "University of Guelph"),
#         ("Concordia", "Concordia University"),
#         ("Dalhousie", "Dalhousie University"),
#         ("Acadia", "Acadia University"),
#         ("Lakehead", "Lakehead University"),
#         ("Otech", "Ontario Tech University"),
#         ("TRU", "Thompson Rivers University"),
#         ("VIV", "Vancouver Island University"),
#         ("ETS", "École de Technologie Supérieure"),
#         ("UPEI", "University of Prince Edward Island"),
#         ("OCAD", "OCAD University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University"),
#         ("UduQAT", "Université du Québec en Abitibi-Témiscamingue"),
#         ("Au", "Algoma University"),
#         ("YU", "Yorkville University"),
#         ("STU", "St. Thomas University"),
#         ("ENAP", "École Nationale d'Administration Publique"),
#         ("USB", "Université de Saint-Boniface"),
#         ("CUE", "Concordia University of Edmonton"),
#         ("NSCAD", "NSCAD University"),
#         ("Ru", "Redeemer University"),
#         ("UCanWest", "University Canada West"),
#         ("UofKC", "University of King's College"),
#         ("CU", "Canadian Mennonite University"),
#         ("KU", "The King's University"),
#         ("AU", "Ambrose University"),
#         ("USA", "Université Sainte-Anne"),
#         ("FNU", "First Nations University of Canada"),
#         ("QUC", "Quest University Canada"),
#         ("BU", "Brandon University"),
#         ("BSU", "Bishop's University"),
#         ("UduQO", "Université du Québec en Outaouais"),
#         ("NSU", "Nipissing University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University"),
#         ("UduQAT", "Université du Québec en Abitibi-Témiscamingue"),
#         ("Au", "Algoma University"),
#         ("YU", "Yorkville University"),
#         ("STU", "St. Thomas University"),
#         ("ENAP", "École Nationale d'Administration Publique"),
#         ("USB", "Université de Saint-Boniface"),
#         ("CUE", "Concordia University of Edmonton"),
#         ("NSCAD", "NSCAD University"),
#         ("Ru", "Redeemer University"),
#         ("UCanWest", "University Canada West"),
#         ("UofKC", "University of King's College"),
#         ("CU", "Canadian Mennonite University"),
#         ("KU", "The King's University"),
#         ("AU", "Ambrose University"),
#         ("USA", "Université Sainte-Anne"),
#         ("FNU", "First Nations University of Canada"),
#         ("QUC", "Quest University Canada"),
#         ("BU", "Brandon University"),
#         ("BSU", "Bishop's University"),
#         ("UduQO", "Université du Québec en Outaouais"),
#         ("NSU", "Nipissing University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University"),
#         ("UduQAT", "Université du Québec en Abitibi-Témiscamingue"),
#         ("Au", "Algoma University"),
#         ("YU", "Yorkville University"),
#         ("STU", "St. Thomas University"),
#         ("ENAP", "École Nationale d'Administration Publique"),
#         ("USB", "Université de Saint-Boniface"),
#         ("CUE", "Concordia University of Edmonton"),
#         ("NSCAD", "NSCAD University"),
#         ("Ru", "Redeemer University"),
#         ("UCanWest", "University Canada West"),
#         ("UofKC", "University of King's College"),
#         ("CU", "Canadian Mennonite University"),
#         ("KU", "The King's University"),
#         ("AU", "Ambrose University"),
#         ("USA", "Université Sainte-Anne"),
#         ("FNU", "First Nations University of Canada"),
#         ("QUC", "Quest University Canada"),
#         ("BU", "Brandon University"),
#         ("BSU", "Bishop's University"),
#         ("UduQO", "Université du Québec en Outaouais"),
#         ("NSU", "Nipissing University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University"),
#         ("UduQAT", "Université du Québec en Abitibi-Témiscamingue"),
#         ("Au", "Algoma University"),
#         ("YU", "Yorkville University"),
#         ("STU", "St. Thomas University"),
#         ("ENAP", "École Nationale d'Administration Publique"),
#         ("USB", "Université de Saint-Boniface"),
#         ("CUE", "Concordia University of Edmonton"),
#         ("NSCAD", "NSCAD University"),
#         ("Ru", "Redeemer University"),
#         ("UCanWest", "University Canada West"),
#         ("UofKC", "University of King's College"),
#         ("CU", "Canadian Mennonite University"),
#         ("KU", "The King's University"),
#         ("AU", "Ambrose University"),
#         ("USA", "Université Sainte-Anne"),
#         ("FNU", "First Nations University of Canada"),
#         ("QUC", "Quest University Canada"),
#         ("BU", "Brandon University"),
#         ("BSU", "Bishop's University"),
#         ("UduQO", "Université du Québec en Outaouais"),
#         ("NSU", "Nipissing University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University"),
#         ("UduQAT", "Université du Québec en Abitibi-Témiscamingue"),
#         ("Au", "Algoma University"),
#         ("YU", "Yorkville University"),
#         ("STU", "St. Thomas University"),
#         ("ENAP", "École Nationale d'Administration Publique"),
#         ("USB", "Université de Saint-Boniface"),
#         ("CUE", "Concordia University of Edmonton"),
#         ("NSCAD", "NSCAD University"),
#         ("Ru", "Redeemer University"),
#         ("UCanWest", "University Canada West"),
#         ("UofKC", "University of King's College"),
#         ("CU", "Canadian Mennonite University"),
#         ("KU", "The King's University"),
#         ("AU", "Ambrose University"),
#         ("USA", "Université Sainte-Anne"),
#         ("FNU", "First Nations University of Canada"),
#         ("QUC", "Quest University Canada"),
#         ("BU", "Brandon University"),
#         ("BSU", "Bishop's University"),
#         ("UduQO", "Université du Québec en Outaouais"),
#         ("NSU", "Nipissing University"),
#         ("MSVU", "Mount Saint Vincent University"),
#         ("UQAR", "Université du Québec à Rimouski"),
#         ("ECD", "Emily Carr University of Art and Design"),
#         ("RMC", "Royal Military College of Canada"),
#         ("CapU", "Capilano University"),
#         ("CBU", "Cape Breton University")
#     ]

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
    occupation = models.CharField(max_length=255, choices=OCCUPATION_TYPES)

    def str(self):
        return f"Property Owner Profile - {self.first_name}"