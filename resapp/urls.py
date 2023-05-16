from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("prop",views.index,name="prop"),
    path("l",views.login,name="l"),
   path("buy",views.buy,name="buy"),
   path("book",views.bookings,name="book"),
    path("dashboard2",views.dashboard2,name="dashboard2"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("booki",views.register,name="booki"),
    path("lr",views.hlr,name="lr"),
    path("sell",views.sell,name="sell"),
    path("logout",views.logout,name="logout"),
    path("review",views.review_properties,name="review"),
    path('send-email',views.send_email,name="send-email" ),
    path('charge/', views.charge, name="charge"),
    path('payment.html', views.payment, name='payment'),
    path('delete_booking/', views.delete_booking, name='delete_booking'),



]