from django.contrib import admin
from django.urls import path 
from record import views

urlpatterns = [
    path('', views.index, name='home'),
    path('postsignup/', views.postsignup, name='postsignup'),
    path('signUp/', views.signUp, name='signup'),
    path('signIn/', views.signIn, name='signin'),
    path('postSignIn/', views.postSignIn, name = 'postSignIn'),
    path('postReset/', views.postReset, name='postreset'),
    path('reset/', views.reset, name='reset'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('Notification-Center/', views.notification, name='Notification-Center'), 
    path('user-logout/',views.logout,name='logout'),
   
   
]