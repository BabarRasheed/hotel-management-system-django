import datetime
from hotel.models import Room, Reservation

def check_availability(room, reservation_date, reservation_date_out):
    avail_list=[]
    Booking_list = Reservation.objects.filter(room=room)
    for booking in Booking_list:
        if booking.reservation_date > reservation_date_out or booking.reservation_date_out < reservation_date:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)