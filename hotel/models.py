from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField
from djmoney.models.fields import MoneyField
import random
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

GENDER = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Other", "Other"),
)

IDENTITY_TYPE = (
    ("National ID Number", "National ID Number"),
    ("Driver's License", "Driver's License"),
    ("International Passport", "International Passport"),
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

def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user.id, filename)

def rooms(instance, filename):
    # Assuming you want to save files in a folder named 'uploads' within your MEDIA_ROOT
    return os.path.join('rooms', filename)

class ContactUs(models.Model):
    name=models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    email=models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.name

class User(AbstractUser):
    user_number = models.PositiveIntegerField(unique=True, null=True, blank=True)
    isAdmin = models.BooleanField('Is Admin', default=False)
    isCustomer = models.BooleanField('Is Customer', default=False)
    isEmployee = models.BooleanField('Is Employee', default=False)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=500, unique=True)
    email = models.EmailField( unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    profile_picture = models.ImageField(upload_to="images/", default="images/id.jpg", null=True, blank=True)   

    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.ImageField(upload_to="image/", default="images/id.jpg", null=True, blank=True)

    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    wallet = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', default=500000.00)
    verified = models.BooleanField(default=False)
    guest = models.BooleanField(default=False)
    
    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.user_number:
            # Generate a unique user number based on the maximum existing number
            max_user_number = User.objects.aggregate(models.Max('user_number'))['user_number__max']
            if max_user_number is not None:
                self.user_number = max_user_number + 1
            else:
                self.user_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Code(models.Model):
    number = models.CharField(max_length=15, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)

class Profile(models.Model):
    #pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz123")
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.FileField(upload_to=user_directory_path, default="id.jpg", null=True, blank=True)   

    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"
        
""" choices=ROOM_CHOICES, default='Greed Hotel' """

def rooms(instance, filename):
    return f'rooms/{filename}'

class Reservation(models.Model):

    booking_number = models.PositiveIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    room = models.CharField(max_length=100)  
    reservation_date = models.DateTimeField(null=True, blank=True)
    reservation_date_out = models.DateTimeField(null=True, blank=True,)
    party_size = models.PositiveIntegerField(null=True, blank=True)
    special_requests = models.TextField(blank=True)
    wallet = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', default=0.00)
    price = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', default=0.00)
    change = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', default=0.00)
    approval_status = models.BooleanField("approve", default=False)
    approval_comment = models.CharField(max_length=100, default="Waiting for Approval")
    checked = models.BooleanField("admin checked", default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if not self.booking_number:
            # Generate a unique booking number based on the maximum existing number
            max_booking_number = Reservation.objects.aggregate(models.Max('booking_number'))['booking_number__max']
            if max_booking_number is not None:
                self.booking_number = max_booking_number + 1
            else:
                self.booking_number = 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"


@receiver(pre_delete, sender=Reservation)
def update_room_availability(sender, instance, **kwargs):
    # When a Reservation is deleted, update the corresponding Room's availability
    if instance.room:
        try:
            room = Room.objects.get(name=instance.room)
            room.available = True
            room.save()
        except Room.DoesNotExist:
            # Handle the case where the room associated with the reservation doesn't exist
            pass

class Room(models.Model):
    book_count = models.PositiveIntegerField(default=0)
    tag = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=12, decimal_places=2, default_currency='PHP', default=0.00)
    image = models.FileField(upload_to=rooms, default="default.jpg")
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    reservation = Reservation

    def __str__(self):
        return self.name

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         #Reservation.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)