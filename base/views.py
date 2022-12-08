from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
# Create your views here.



def home(request):
    if request.user.is_authenticated:
        searched_entries = Entry.objects.filter(host = request.user)
        if request.method=='POST':
            searched = request.POST['searched']
            searched_entries = searched_entries.filter(Q(record__contains=searched)| Q(highlight__contains=searched))
            
        
            
        return render(request, 'base/home.html',{'searched_entries':searched_entries})
        
    else:
        return render(request, 'base/home.html')


   

@login_required(login_url='login')
def createEntry(request):
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request)
        Entry.objects.create(
            host = request.user,
            record=request.POST.get('record'),
            highlight=request.POST.get('highlight'),
            mood = request.POST.get('mood')
            
        )
        return redirect('home')
        


    return render(request, 'base/create-entry.html', {'form':form})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form}) 


def logoutUser(request):
    logout(request)
    return redirect('home')


def calendar(request):
    return render(request, 'base/calendar_module.html')