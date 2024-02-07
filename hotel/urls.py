from django.urls import path
from hotel import views

app_name = "hotel"

urlpatterns = [

    path('signup/', views.RegisterView, name='signup'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('book/', views.BookingView, name='book'),
    path('profile/<user_id>', views.ProfileView, name='profile'),
    path('contactus/', views.ContactUsView, name='contactus'),
    path('aboutus/', views.AboutUsView, name='aboutus'),
    path('listbooking/', views.ListBooking, name='listbooking'),
    path('listreserve/', views.ListReserve, name='listreserve'),
    path('showbooking/<booking_id>', views.ShowBooking, name='showbooking'),
    path('showreserve/<booking_id>', views.ShowReserve, name='showreserve'),
    path('updatebooking/<booking_id>', views.UpdateBooking, name='updatebooking'),
    path('deletebooking/<booking_id>', views.DeleteBooking, name='deletebooking'),
    path('verify/', views.verify_view, name='verify-view'),
    path('verify2/', views.CodeVerify, name='verify2'),
    #path('login', views.login, name = 'login'),
    #path('register', views.register, name='register'),
    #path('home', views.home, name='home'),

]