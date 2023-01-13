from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from datetime import date
# Create your views here.



def home(request):
    if request.user.is_authenticated:
        searched_entries = Entry.objects.filter(host = request.user)
        if request.method=='POST':
            if 'searched' in request.POST:
                searched = request.POST['searched']
                searched_entries = searched_entries.filter(Q(record__contains=searched)| Q(highlight__contains=searched))
                context={'searched_entries':searched_entries.order_by('-created_at'), 'searched':searched}  
            elif 'pickdate' in request.POST:
                page = 'calendar'
                today = date.today()
                today = today.strftime('%Y-%m-%d')
                if request.user.is_authenticated:
                    selected_date = Entry.objects.filter(host = request.user)
                    if request.method=='POST':
                        pickdate = request.POST['pickdate']
                        if pickdate:
                            selected_date = selected_date.filter(Q(created_at=pickdate))
                            return render(request, 'base/home.html',{'today':today, 'selected_date':selected_date, 'page':page})
                        else:
                            return HttpResponse('Select date')
                    else:
                        return render(request, 'base/home.html',{'today':today,'page':page})
                else:
                
                    return redirect('login')

            
        else:
            context={'searched_entries':searched_entries}
        
        
        return render(request, 'base/home.html',context=context)
    else:
        return render(request, 'base/home.html')       
        
@login_required(login_url='login')
def entryLog(request):
    page = 'entry-log'
    if request.user.is_authenticated:
        searched_entries = Entry.objects.filter(host = request.user)
        paginator = Paginator(searched_entries, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if request.method=='POST':
            searched = request.POST['searched']
            searched_entries = searched_entries.filter(Q(record__contains=searched)| Q(highlight__contains=searched))
            paginator = Paginator(searched_entries, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context={'page_obj':page_obj, 'searched':searched,'page':page}  
           

            
        else:
            context={'searched_entries':searched_entries,'page':page, 'page_obj':page_obj}
        
        
        return render(request, 'base/home.html',context=context)
    else:
        return render(request, 'base/home.html')   
   

@login_required(login_url='login')
def createEntry(request):
    page='create-entry'
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request)
        Entry.objects.create(
            host = request.user,
            record=request.POST.get('record'),
            highlight=request.POST.get('highlight')
            
        )
        return redirect('home')
        


    return render(request, 'base/home.html', {'form':form,'page':page})


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

    # if request.method=='POST':
    #     form = MyUserCreationForm(request.POST)
    #     User.objects.create(
    #         name = request.POST.get('name'),
    #         username = request.POST.get('username'),
    #         email = request.POST.get('email'),
    #         password = request.POST.get('password'),
           
    #     )


    return render(request, 'base/login_register.html', {'form': form}) 


def logoutUser(request):
    logout(request)
    return redirect('home')


def calendarSearch(request):
    page = 'calendar'
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    if request.user.is_authenticated:
        selected_date = Entry.objects.filter(host = request.user)
        if request.method=='POST':
            pickdate = request.POST['pickdate']
            if pickdate:
                selected_date = selected_date.filter(Q(created_at=pickdate))
                return render(request, 'base/home.html',{'today':today, 'selected_date':selected_date, 'page':page})
            else:
                return HttpResponse('Select date')
        else:
            return render(request, 'base/home.html',{'today':today,'page':page})
    else:
       
        return redirect('login')

    

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('update-user')

    return render(request, 'base/update_user.html', {'form': form})


@login_required(login_url = 'login')
def updateEntry(request, pk):
    page = 'update-entry'
    entry = Entry.objects.get(id=pk)
    form = EntryForm(instance = entry)
    
    if request.method=='POST':
        form = EntryForm(request.POST, instance = entry)
        if entry.host == request.user:
            if form.is_valid():
                form.save()
                return redirect('entry-log')
            # return render(request, 'base/home.html', {'form':form, 'page':page, 'entry':entry})
        else:
            return HttpResponse('You are not authorized to edit this...')
    return render(request, 'base/home.html', {'form':form, 'page':page, 'entry':entry})
    
    
    
def deleteEntry(request,pk):
    
    entry = Entry.objects.get(id=pk)
    if entry.host == request.user:
        if request.method=='POST':
            entry.delete()
            return redirect('entry-log')
    else:
        return HttpResponse('Unauthorised User...')
    return render(request, 'base/delete.html', {'obj':entry})

