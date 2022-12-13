from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('',views.home, name='home'),

    path('create-entry/', views.createEntry, name='create-entry'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/',views.logoutUser, name='logout'), 
    path('calendar/',views.calendarSearch, name='calendarSearch'),
    path('entry-log/', views.entryLog, name='entry-log'), 
    path('update-user/', views.updateUser, name='update-user'),
    path('update-entry/<str:pk>', views.updateEntry, name='update-entry'),
    path('delete/<str:pk>/',views.deleteEntry, name='delete'), 
    # path('create-entry/', views.createEntry, name='createEntry')
    ]