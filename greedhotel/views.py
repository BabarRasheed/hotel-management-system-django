from django.shortcuts import render
from hotel.models import User, Reservation, ContactUs, Room

def base(request):
    profileId = User.objects.all() 
    return render(request, "partials/base.html", {'profileId': profileId})

def index(request):
    return render(request, "hotel/home.html")