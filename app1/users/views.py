from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from traitlets import Instance
from bascket.models import Bascket
from users.forms import Profileform, User_loginform, User_registrform
from django.urls import reverse
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = User_loginform(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f'{username}, вы вошли в аккаунт')

                if session_key:
                    Bascket.objects.filter(session_key=session_key).update(user=user)

                redirect_page= request.POST.get('next', None)
                if redirect_page and redirect_page!=reverse('user:logout'):
                     return HttpResponseRedirect(request.POST.get('next')) #редирект на нужную страницу после авторизации мы идём по указанной ссылке, а не как обычно на index
                
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

                session_key = request.session.session_key

                user = form.instance
                auth.login(request, user)

                if session_key:
                    Bascket.objects.filter(session_key=session_key).update(user=user)

                messages.success(request, f'{user.username}, вы успешно зарегистрировались и вы вошли в аккаунт')
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = User_registrform()
    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)

@login_required #нужно для запрета анонимным пользователям открывать приложения не доступные без юзера
def profile(request):

    if request.method == 'POST':
        form = Profileform(data=request.POST, instance=request.user, files=request.FILES)
        
        if form.is_valid():
                form.save()
                messages.success(request, "Профель успещно обновлён")
                return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = Profileform(instance=request.user)

    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }

    return render(request, 'users/profile.html', context)

def users_cart(request):
     return render(request, 'users/users-cart.html')

@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, вы вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))