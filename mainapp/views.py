from django.shortcuts import render

from .models import Property, OwnerUser

def landingpage(request):
    ouser = OwnerUser.objects.all()
    return render(request, 'mainapp/landing-page.html', {'ouser':ouser})
