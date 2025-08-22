from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth
from users.forms import User_loginform, User_registrform
from django.urls import reverse
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = User_loginform(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = User_loginform()
        
    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }

    return render(request, 'users/login.html', context)


def registration(request):
    
    if request.method == 'POST':
        form = User_registrform(data=request.POST)
        if form.is_valid():
                form.save()
                user = form.instance
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = User_registrform()
    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'Home - Кабинет',
    }

    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)


    return redirect(reverse('main:index'))