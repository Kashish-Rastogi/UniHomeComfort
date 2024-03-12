from django.urls import path
from .views import landingpage, loginpage, ownerdashboard

myapp_name = 'mainapp'

urlpatterns = [
    path('', landingpage, name='landing-page'),
    path('login/', loginpage, name='login-page'),
    path('owner-dashboard/', ownerdashboard, name='owner-dashboard'),
]