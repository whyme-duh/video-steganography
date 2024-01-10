from django.shortcuts import render, redirect
from django.contrib import messages
from Users.models import Profile
from . forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from core.models import Encoding

def register(request):
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created succesfully')
            return redirect('login')
        else:
            messages.error(request, f'Error occured. Please Try again!')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form' : form})


def profile(request):
    context={
        'encoded_videos' : Encoding.objects.filter(user = request.user)
    }
    return render(request, 'users/profile.html',context)
