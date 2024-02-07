from django.urls import path
from greedhotel import views

app_name = "greedhotel"

urlpatterns = [

    path('', views.index, name='home'),
    path('base', views.base, name='base'),

    #path('login', views.login, name = 'login'),
    #path('register', views.register, name='register'),
    #path('home', views.home, name='home'),

]

    

    