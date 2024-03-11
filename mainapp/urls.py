from django.urls import path
from .views import landingpage, loginpage

myapp_name = 'mainapp'

urlpatterns = [
    path('', landingpage, name='landing-page'),
    path('login/', loginpage, name='login-page'),
]