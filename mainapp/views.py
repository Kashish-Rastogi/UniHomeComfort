from django.shortcuts import render

from .models import Property, OwnerUser

def landingpage(request):
    ouser = OwnerUser.objects.all()
    return render(request, 'mainapp/landing-page.html', {'ouser':ouser})

def loginpage(request):
    return render(request,'mainapp/login.html')

def ownerdashboard(request):
    return render(request,'mainapp/owner-dashboard.html')