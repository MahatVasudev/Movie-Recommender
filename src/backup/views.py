from django.shortcuts import render
from .models import Users
from .forms import UserForm

# Create your views here.
def my_profile_view(request):
    users = Users.objects.get(user=request.username)
    form = UserForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False 
    
    if form.is_valid():
        form.save()
        confirm = True 
        
    context = {
        'user':users,
        'form':form,
        'confirm':confirm
    }
    return render(request, 'users/main.html', context)