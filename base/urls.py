from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('',views.home, name='home'),

    path('create-entry/', views.createEntry, name='create-entry'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/',views.logoutUser, name='logout'), 
    path('calendar/',views.calendar, name='calendar')
    # path('create-entry/', views.createEntry, name='createEntry')
    ]