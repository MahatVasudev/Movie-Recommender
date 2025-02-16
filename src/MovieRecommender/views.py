from django.shortcuts import render, redirect
from Profile.models import WatchList
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def logout_view(request):
    logout(request)
    return redirect('/login')

def login_view(request):
    error_message = None 
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password = password)
            if user is not None:
                login(request,user)
                new_acc = WatchList.objects.filter(uid=request.user)
                if len(new_acc) == 0:
                    return redirect('Movies:description')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('Movies:home')
                
        else:
            error_message = "Oops .. something went wrong"
            
    context = {
        'form': form,
        'error_message': error_message
    }
    
    return render(request,'auth/login.html', context)

def create_account(request):
    error_message = None
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            
            if password1 == password2:
                User.objects.create(username=username, password= make_password(password1))
                return redirect("Movies:home")
            else:
                error_message = "Passwords dont match"
                
        else:
            error_message = "Oops something isn't right"
    context = {
        'form':form,
        'error_message':error_message
    }
    
    return render(request, "auth/create_user.html", context)
            
            
