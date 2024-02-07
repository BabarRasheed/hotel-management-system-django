from django.contrib import admin
from hotel.models import User, Reservation, ContactUs, Room, Code

class UserAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['user_number', 'username', 'full_name', 'email', 'phone', 'gender', 'wallet', 'verified']

class ReservationAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'user__username']
    list_display = ['booking_number', 'full_name', 'room', 'reservation_date', 'reservation_date_out', 'party_size', 'special_requests', 'price', 'change', 'approval_status', 'approval_comment', 'checked']

class ContactUsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'subject']
    list_display = ['name', 'subject', 'email']

class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'available']
    list_display = ['book_count', 'name', 'price', 'available']

class CodeAdmin(admin.ModelAdmin):
    search_fields = ['code', 'user']
    list_display = ['user']

admin.site.register(User, UserAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Code, CodeAdmin)