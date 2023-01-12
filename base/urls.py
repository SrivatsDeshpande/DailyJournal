from django.urls import path
from django.contrib.auth import views as auth_views

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


    path('reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
    ]