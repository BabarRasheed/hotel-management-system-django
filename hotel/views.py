from django.shortcuts import render, redirect
from hotel.models import User, Reservation, ContactUs, Room, Code
from hotel.forms import UserRegisterForm, UserLoginForm, BookingForm, CodeForm, CodeForm2, Approval
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
import re
from datetime import datetime, date
from django.core.mail import send_mail
from django.conf import settings
from greed import settings
from djmoney.money import Money

@login_required(login_url='/user/login/')
def CodeVerify(request):

    form = CodeForm2(request.POST or None)

    id = request.user.id

    code = Code.objects.filter(user=id)

    code = code.first()
    
    if request.method == "POST":
        if 'displayCodeBtn' in request.POST:
            
            messages.success(request, f'Your Code: {code}')

        else:
            if form.is_valid():
                
                username = form.cleaned_data.get('username')
                num = form.cleaned_data.get('number')

                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = None

                if user is not None:
                    stored_code = user.code

                    if str(stored_code) == num:
                        user.verified = True
                        user.guest = False
                        user.save()
                        messages.success(request, f"{user.full_name}, you are now verified.")
                        return redirect('greedhotel:home')
                    else:
                        messages.error(request, "Invalid Verification Code")
                else:
                    messages.error(request, "User not found with the provided username")
    return render(request, "userauth/verify2.html", {'form': form})

def ContactUsView(request):

    

    if request.method == "POST":
        contact=ContactUs()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact.name=name
        contact.email=email
        contact.subject=subject
        contact.message=message

        contact.save()
        messages.success(request, f"Thank you for your feedback.")
        return redirect('greedhotel:home')

    return render(request, 'hotel/contactus.html')

@login_required(login_url='/user/login/')
def LogoutView(request):
    logout(request)
    return redirect("greedhotel:home")

def LoginView(request):

    form = UserLoginForm(request.POST or None)

    context = {
        "form":form,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.verified == True:
                auth.login(request, user)
                return redirect("greedhotel:home")
            else:
                auth.login(request, user)
                if user.guest == True:
                    messages.error(request, f"{user.full_name}, you still have a GUEST account because it has not been verified yet.")
                    return redirect("greedhotel:home")
                else:
                    messages.error(request, f"{user.full_name}, your account has not been verified yet.")
                    return redirect("greedhotel:home")
        else:
            messages.error(request, "Invalid login details.")
    return render(request, "userauth/authlog.html", context)

def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("greedhotel:home")

    if request.method =="POST":
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            print("Success")
            form.save()
            full_name = form.cleaned_data.get("full_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password1")

            user = authenticate(email=email, password=password)

            messages.success(request, f"Hey {full_name}, we need your verification code to complete your registration.")

            if user is not None:
                request.session['pk'] = user.pk
                return redirect("hotel:verify-view")
    else:
        form = UserRegisterForm()

    context = {
        "form":form,
    }

    return render(request, "userauth/authreg.html", context)

def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        email = user.email
        code = user.code
        sender = 'isoygwapo84@gmail.com'
        code_user = f"{user.username}: {user.code}"
        subject = "[Greed's Hotel] Verification Code"

        message = f'The code is required for further verification if you want to verify your account. To complete the registration, enter the verification code provided. \n\n\nVerification Code: {code}'

        # Use a list or tuple for the "to" argument
        recipient_list = [email]

        send_mail(subject, message, sender, recipient_list)
        
        if not request.POST:
            print(code_user, email) 
            #send SMS code
        if form.is_valid():
            num = form.cleaned_data.get('number')
            
            if str(code) == num:
                user.verified = True
                user.guest = False
                user.save()
                code.save()
                if user is not None:
                    request.session['pk'] = user.pk
                    messages.success(request, f"{user.full_name}, you are now verified.")
                    return redirect('hotel:login')
            else:
                messages.error(request, "Invalid Verification Code")
    return render(request, "userauth/verify.html", {'form': form})

def deduction_room_price(room, money):
    if room == "Room-Only Hotel Rooms":
        price = Money(7500, 'PHP') 
        return money - price
    elif room == "Standard Hotel Rooms":
        price = Money(12500, 'PHP')
        return money - price
    elif room == "Minimalist Hotel Rooms":
        price = Money(10000, 'PHP')
        return money - price
    elif room == "Deluxe Hotel Rooms":
        price = Money(20000, 'PHP')
        return money - price
    elif room == "Standard Suite Rooms":
        price = Money(25000, 'PHP')
        return money - price
    elif room == "Presidential Suites":
        price = Money(100000, 'PHP')
        return money - price
    elif room == "Penthouse Suites":
        price = Money(150000, 'PHP')
        return money - price
    elif room == "Honeymoon Suites":
        price = Money(25000, 'PHP')
        return money - price
    
def decline_room_price(room, money):
    if room == "Room-Only Hotel Rooms":
        price = Money(7500, 'PHP')  
        return money + price
    elif room == "Standard Hotel Rooms":
        price = Money(12500, 'PHP')
        return money + price
    elif room == "Minimalist Hotel Rooms":
        price = Money(10000, 'PHP')
        return money + price
    elif room == "Deluxe Hotel Rooms":
        price = Money(20000, 'PHP')
        return money + price
    elif room == "Standard Suite Rooms":
        price = Money(25000, 'PHP')
        return money + price
    elif room == "Presidential Suites":
        price = Money(100000, 'PHP')
        return money + price
    elif room == "Penthouse Suites":
        price = Money(150000, 'PHP')
        return money + price
    elif room == "Honeymoon Suites":
        price = Money(25000, 'PHP')
        return money + price

def get_price(room):
    if room == "Room-Only Hotel Rooms":
        price = Money(7500, 'PHP')
        return price
    elif room == "Standard Hotel Rooms":
        price = Money(12500, 'PHP')
        return price
    elif room == "Minimalist Hotel Rooms":
        price = Money(10000, 'PHP')
        return price
    elif room == "Deluxe Hotel Rooms":
        price = Money(20000, 'PHP')
        return price
    elif room == "Standard Suite Rooms":
        price = Money(25000, 'PHP')
        return price
    elif room == "Presidential Suites":
        price = Money(100000, 'PHP')
        return price
    elif room == "Penthouse Suites":
        price = Money(150000, 'PHP')
        return price
    elif room == "Honeymoon Suites":
        price = Money(25000, 'PHP')
        return price

@login_required(login_url='/user/login/')
def ShowReserve(request, booking_id):
    reservations_show = Reservation.objects.get(pk=booking_id) 
    
    form = Approval(request.POST or None, instance=reservations_show)
    if request.method == 'POST':
        status = request.POST.get('approval_status')
        comment = request.POST.get('approval_comment')

        if status == "approved" or status == "declined":
            if status == "approved":
                id = request.POST.get('reservation_id')
                print(id)
                Reservation.objects.filter(booking_number=id).update(approval_status=True)
                Reservation.objects.filter(booking_number=id).update(checked=True)
                Reservation.objects.filter(booking_number=id).update(approval_comment=comment)
                return redirect('hotel:listreserve')
            elif status == "declined":
                id = request.POST.get('reservation_id')
                print(id)
                
                reservation = Reservation.objects.get(booking_number=id)
                username = reservation.user
                user = User.objects.filter(username=username).first()
                money = 0
                money = user.wallet 
                print(money)
                room = reservation.room
                refund = decline_room_price(room, money)
                print(refund)
                User.objects.filter(username=username).update(wallet=refund)
                Reservation.objects.filter(booking_number=id).update(approval_comment=False)
                Reservation.objects.filter(booking_number=id).update(checked=True)
                Reservation.objects.filter(booking_number=id).update(approval_comment=comment)

                Room.objects.filter(name=room).update(available=True)
                return redirect('hotel:listreserve')
            else:
                messages.info(request, 'Invalid Input.')
        else:
            messages.info(request, 'Fields should not be blank.')

    return render(request, 'hotel/showreserve.html', {'reservations_show': reservations_show, 'form': form})

def BookingView(request):

    hotel = Room.objects.all() 

    emailVal = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    reservation = Reservation.objects.all()

    roomdefault = ["Greed Hotel"]
    data = []

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        room = request.POST.get('room')
        party_size = request.POST.get('party_size')
        check_in = request.POST.get('reservation_date')
        check_out = request.POST.get('reservation_date_out')
        special_requests = request.POST.get('special_requests')

        data = [full_name, username, email, password, phone, room, party_size, check_in, check_out, special_requests]
        roomdefault = [room]

        if room:
            try:
                roomall = Room.objects.get(name=room)
            except Room.DoesNotExist:
                pass
        
        
        print(data)
        if full_name == "" or email == "" or phone == "" or room == "" or party_size == "":
            messages.info(request, 'Fields should not be blank.')
        elif not re.match(emailVal, email):
            messages.error(request, 'Invalid Email Format.')
        elif username == "":
            messages.error(request, 'Invalid Username Input')
        elif room == "Greed Hotel":
            messages.error(request, 'Please Select A Valid Room.')
        elif party_size == "":
            messages.error(request, 'Invalid Table Input.')
        elif password == "":
            messages.error(request, 'Invalid Password.')
        else:
            if check_in and check_out:

                check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
                check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

                check_in_aware = timezone.make_aware(check_in, timezone=timezone.get_current_timezone())
                check_out_aware = timezone.make_aware(check_out, timezone=timezone.get_current_timezone())

                if check_in_aware.date() < date.today():
                    messages.error(request, 'Booking Date Should Not Be Before Today.')
                elif check_in_aware > check_out_aware:
                    messages.error(request, 'Booking Date Should Not Be Before Check-Out Date.')
                else:

                    user = authenticate(email=email, password=password)

                    avail_list=[]
                    # Booking_list = Reservation.objects.filter(room=room)
                    for r in reservation:
                        if r.room == room:
                            overlapping_bookings = Reservation.objects.filter(
                                booking_number=r.booking_number,
                                room=r.room,
                                reservation_date__lte=check_out_aware,
                                reservation_date_out__gte=check_in_aware
                            )
                            if overlapping_bookings.exists():
                                avail_list.append(True)
                            else:
                                avail_list.append(False)

                    # overlapping_bookings = Reservation.objects.filter(
                    #     room=room,
                    #     reservation_date__lte=check_out_aware,
                    #     reservation_date_out__gte=check_in_aware
                    # )
                    print(avail_list)
                    # if overlapping_bookings.exists():
                    if any(avail_list):
                        messages.error(request, 'Someone Has Already Booked For That Date.')
                    else:
                        user = User.objects.filter(username=username).first()
                        money = 0
                        if request.user.is_authenticated:
                            owner = User.objects.get(username=username)
                            money = owner.wallet
                        
                            print(money)
                        
                            price = get_price(room)

                            deduction = deduction_room_price(room, money)
                            print(deduction)

                        else:

                            money = Money(100000, 'PHP')
                        
                            print(money)
                        
                            price = get_price(room)

                            deduction = deduction_room_price(room, money)
                            print(deduction)
                        
                        if user is None:
                            # If the user doesn't exist, create a new one

                            user = User(
                                full_name=full_name,
                                username=username, 
                                email=email,
                                phone=phone,
                                guest=True,
                                )

                            user.set_password(password)

                            user.save()

                        
                        print(full_name, email, phone, room, check_in, check_out, party_size, special_requests)
                        if money < price:
                            messages.error(request, 'Not enough money.')
                        elif request.user.is_authenticated:
                            User.objects.filter(email=email).update(wallet=deduction)

                            book_count = roomall.book_count + 1
                            Room.objects.filter(name=room).update(book_count=book_count)

                            reservation = Reservation(
                                    full_name=full_name,
                                    email=email,
                                    phone=phone,
                                    room=room,
                                    reservation_date=check_in,
                                    reservation_date_out=check_out,
                                    party_size=party_size,
                                    special_requests=special_requests,
                                    wallet=money,
                                    price=price,
                                    change=deduction,
                                    username=username,
                                    user=user
                                )
                        else:
                            User.objects.filter(email=email).update(wallet=deduction)

                            book_count = roomall.book_count + 1
                            Room.objects.filter(name=room).update(book_count=book_count)

                            reservation = Reservation(
                                    full_name=full_name,
                                    email=email,
                                    phone=phone,
                                    room=room,
                                    reservation_date=check_in,
                                    reservation_date_out=check_out,
                                    party_size=party_size,
                                    special_requests=special_requests,
                                    wallet=money,
                                    price=price,
                                    change=deduction,
                                    username=username,
                                    user=user
                                )

                        reservation.save()

                        Room.objects.filter(name=room).update(available=False)

                        messages.success(request, 'Successfully Booked.')
                        return redirect('hotel:book')
            else:
                messages.error(request, 'Invalid Date Format.')

    return render(request, "hotel/rooms.html", {'reservation': reservation, 'hotel': hotel, 'data': data, 'roomdefault': roomdefault})

def check_availability(room, reservation_date, reservation_date_out):
    avail_list=[]
    Booking_list = Reservation.objects.filter(room=room)
    for booking in Booking_list:
        if booking.reservation_date > reservation_date_out or booking.reservation_date_out < reservation_date:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)

@login_required(login_url='/user/login/')
def ListBooking(request):
    reservations_list = Reservation.objects.all() 
    return render(request, 'hotel/listbooking.html', {'reservations_list': reservations_list})

@login_required(login_url='/user/login/')
def ShowBooking(request, booking_id):
    reservations_show = Reservation.objects.get(pk=booking_id) 
    return render(request, 'hotel/showbooking.html', {'reservations_show': reservations_show})

@login_required(login_url='/user/login/')
def UpdateBooking(request, booking_id):
    reservation_update = Reservation.objects.get(pk=booking_id)
    data = []
    hotel = Room.objects.all()
    if request.method == 'POST':
            username = reservation_update.username
            room = request.POST.get('room')
            party_size = request.POST.get('party_size')
            check_in = request.POST.get('reservation_date')
            check_out = request.POST.get('reservation_date_out')
            special_requests = request.POST.get('special_requests')
            
            data = [check_in, check_out]
            if check_in and check_out:

                check_in = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
                check_out = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')

                check_in_aware = timezone.make_aware(check_in, timezone=timezone.get_current_timezone())
                check_out_aware = timezone.make_aware(check_out, timezone=timezone.get_current_timezone())

                if check_in_aware.date() < date.today():
                    messages.error(request, 'Booking Date Should Not Be Before Today.')
                elif check_in_aware > check_out_aware:
                    messages.error(request, 'Booking Date Should Not Be Before Check-Out Date.')
                else:

                    reservation = Reservation.objects.all()
                    avail_list=[]

                    for r in reservation:
                        if r.room == room:
                            overlapping_bookings = Reservation.objects.filter(
                                booking_number=r.booking_number,
                                room=r.room,
                                reservation_date__lte=check_out_aware,
                                reservation_date_out__gte=check_in_aware
                            )
                            if overlapping_bookings.exists():
                                avail_list.append(True)
                            else:
                                avail_list.append(False)

                    print(avail_list)

                    if any(avail_list):
                        messages.error(request, 'Someone Has Already Booked For That Date.')
                    else:
                        id = request.POST.get('reservation_id')

                        current_room = request.POST.get('prevroom')
                        print(current_room)
                        Room.objects.filter(name=current_room).update(available=True)

                        new_room = request.POST.get('room')
                        print(new_room)
                        Room.objects.filter(name=new_room).update(available=False)
                        
                        ##################CALCULATIONS#################

                        owner = User.objects.get(username=username)
                        money = owner.wallet
                    
                        print(money)
                    
                        price = get_price(current_room)
                        print(money)
                        print(price)
                        money = money + price
                        print(money)


                        reservation = Reservation.objects.get(booking_number=id)
                        username = reservation.user
                        user = User.objects.filter(username=username).first()
                        price = get_price(new_room)

                        room = new_room
                        new_deduction = deduction_room_price(room, money)
                        
                        print(new_deduction)

                        User.objects.filter(username=username).update(wallet=new_deduction)
                        ###############################################

                        Reservation.objects.filter(booking_number=id).update(wallet=money)
                        Reservation.objects.filter(booking_number=id).update(price=price)
                        Reservation.objects.filter(booking_number=id).update(change=new_deduction)

                        Reservation.objects.filter(booking_number=id).update(room=room)
                        Reservation.objects.filter(booking_number=id).update(reservation_date=check_in)
                        Reservation.objects.filter(booking_number=id).update(reservation_date_out=check_out)
                        Reservation.objects.filter(booking_number=id).update(party_size=party_size)
                        Reservation.objects.filter(booking_number=id).update(special_requests=special_requests)
                        Reservation.objects.filter(booking_number=id).update(approval_status=False)
                        Reservation.objects.filter(booking_number=id).update(checked=False)
                        Reservation.objects.filter(booking_number=id).update(approval_comment="Waiting For Approval")

                        messages.success(request, 'Booking Updated.')

                        return redirect('hotel:listbooking')
            else:
                messages.error(request, 'Invalid Date Format')
    return render(request, 'hotel/updatebooking.html', {'reservation_update': reservation_update, 'hotel': hotel, 'data': data})

@login_required(login_url='/user/login/')
def DeleteBooking(request, booking_id):
    reservations_delete = Reservation.objects.get(pk=booking_id) 

    username = reservations_delete.user
    room = reservations_delete.room

    user = User.objects.filter(username=username).first()
    price = get_price(room)
    
    print(price)

    refunded = user.wallet + price

    User.objects.filter(username=username).update(wallet=refunded)

    current_room = reservations_delete.room
    print(current_room)
    Room.objects.filter(name=current_room).update(available=True)

    reservations_delete.delete()

    messages.error(request, 'Booking Deleted.')
    return redirect('hotel:listbooking')

@login_required(login_url='/user/login/')
def ListReserve(request):
    reservations_list = Reservation.objects.all() 
    return render(request, 'hotel/listreserve.html', {'reservations_list': reservations_list})

@login_required(login_url='/user/login/')
def ProfileView(request, user_id):
    user = User.objects.get(user_number=user_id) 

    if request.method == "POST":

        id = request.POST.get('user_number')

        full_name = request.POST.get('full_name')
        profile_picture = request.FILES.get('profile_picture')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        city = request.POST.get('city')
        address = request.POST.get('address')
        wallet = request.POST.get('wallet')

        user = User.objects.get(user_number=id)
        user.full_name = full_name
        if profile_picture:
            if user.profile_picture and not user.profile_picture.name.endswith('id.jpg'):
                user.profile_picture.delete()
            user.profile_picture = profile_picture
        user.gender = gender
        user.phone = phone
        user.country = country
        user.city = city
        user.address = address
        user.save()

        messages.success(request, f"Profile Information Updated Successfully.")
        return redirect('greedhotel:home')

    return render(request, 'hotel/edit_profile_form.html')

def AboutUsView(request):
    return render(request, 'hotel/aboutus.html')

"""
def ApproveDecline(request, booking_id):
    reservation_status = Reservation.objects.get(pk=booking_id)

    form = BookingForm(request.POST or None, instance=reservation_status)
    if request.method == 'POST':
        if form.is_valid():

            form.save()

            current_room = request.POST.get('prevroom')
            print(current_room)
            Room.objects.filter(name=current_room).update(available=True)

            new_room = form.cleaned_data['room']
            print(new_room)
            Room.objects.filter(name=new_room).update(available=False)

            messages.error(request, 'Booking Updated.')

            return redirect('hotel:listbooking')
    return redirect('hotel:listreserve', {'form': form, 'reservation_status': reservation_status}) """




"""
from django.shortcuts import render, redirect   
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
            uname=request.POST.get('username')
            mail=request.POST.get('email')
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')

            if uname=='':
                messages.error(request, 'Username should not be blank!')
                return redirect('register')
            elif User.objects.filter(username=uname).exists() or User.objects.filter(email=mail).exists():
                messages.error(request, 'Account already exist!')
                return redirect('register')
            elif mail=='':
                messages.error(request, 'Email should not be blank!')
                return redirect('register')
            elif pass1=='' or pass2=='':
                messages.error(request, 'Password should not be blank!')
                return redirect('register')
            elif pass1!=pass2:
                messages.error(request, 'Password does not match!')
                return redirect('register')
            else:
                my_user=User.objects.create_user(uname,mail,pass1)
                my_user.save()
                return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if username=='':
                messages.error(request, 'Username should not be blank.')
            elif password=='':
                messages.error(request, 'Password should not be blank.')
            else:
                messages.error(request, 'Invalid Credentials.')
                

            if user is not None:    
                auth_login(request, user)
                return redirect('home')
    return render(request, 'login.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html') 

"""