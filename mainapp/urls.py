from django.urls import path
from .views import landingpage

myapp_name = 'mainapp'

urlpatterns = [
    path('', landingpage, name='landing-page'),

]