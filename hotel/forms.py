from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, Form, PasswordInput, ModelForm
from hotel.models import User, Reservation
from .models import Reservation, Code
from djmoney.forms.fields import MoneyField
import os

GENDER = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Other", "Other"),
)

ROOM_CHOICES = [
    ('Greed Hotel', 'Greed Hotel'),
    ('Room-only Hotel Rooms', 'Room-only Hotel Rooms'),
    ('Standard Hotel Rooms', 'Standard Hotel Rooms'),
    ('Minimalist Hotel Rooms', 'Minimalist Hotel Rooms'),
    ('Deluxe Hotel Rooms', 'Deluxe Hotel Rooms'),
    ('Standard Suite Rooms', 'Standard Suite Rooms'),
    ('Presidential Suites', 'Presidential Suites'),
    ('Penthouse Suites', 'Penthouse Suites'),
    ('Honeymoon Suites', 'Honeymoon Suites'),
]

IDENTITY_TYPE = (
    ("National ID Number", "National ID Number"),
    ("Driver's License", "Driver's License"),
    ("International Passport", "International Passport"),
)

def profile_id_upload_to(instance, filename):
    return f'profile_id/{filename}'

class ProfileForm(forms.ModelForm):

    full_name = forms.CharField(max_length=500)
    username = forms.CharField(max_length=500)
    email = forms.EmailField(max_length=500)
    phone = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER, initial="Other")

    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    address = forms.CharField(max_length=1000)

    identity_type = forms.ChoiceField(choices=IDENTITY_TYPE)
    identity_image = forms.FileField()

    facebook = forms.URLField()
    twitter = forms.URLField()

    wallet = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', initial=0.00)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'gender', 'country', 'city', 'address', 'identity_type', 'facebook', 'twitter', 'wallet']

class BookingForm(ModelForm):
    username = forms.CharField(max_length=500)
    full_name = forms.CharField(max_length=500)
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)
    room = forms.ChoiceField(choices=ROOM_CHOICES, initial='Greed Hotel')
    reservation_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    party_size = forms.IntegerField(widget=forms.TextInput(attrs={'type': "number", 'placeholder': "Person", 'min': "1"}))
    special_requests = forms.CharField()

    class Meta:
        model = Reservation
        fields = ['full_name', 'username', 'email', 'phone', 'room', 'reservation_date', 'party_size', 'special_requests']


class UserRegisterForm(UserCreationForm):

    full_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Full Name", 'class': "input-field"}))
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Username", 'class': "input-field"}))
    email = forms.EmailField(label=False, widget=forms.TextInput(attrs={'placeholder': "Email", 'class': "input-field"}))
    phone = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Phone", 'class': "input-field"}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': "input-field"}))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'class': "input-field"}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'type': "email", 'placeholder': "Email", 'class': "input-field"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': "password", 'placeholder': "Password", 'class': "input-field"}))

    class Meta:
        fields = ['username', 'password']


class CodeForm(forms.ModelForm):
    number = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Enter Verification Code", 'class': "input-field"}))
    class Meta:
        model = Code
        fields = ['number'] 
        
class CodeForm2(forms.ModelForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Username", 'class': "input-field"}))

    number = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': "Enter Verification Code", 'class': "input-field"}))
    class Meta:
        model = Code
        fields = ['username', 'number'] 

class Approval(forms.ModelForm):
    
    class Meta(Reservation):
        model = Reservation
        fields = ['approval_status', 'approval_comment']
