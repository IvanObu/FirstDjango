from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.template.context_processors import request
from django.views.generic import CreateView, TemplateView, UpdateView
from bascket.models import Bascket
from orders.models import Order, OrderItem
from users.forms import Profileform, UserRegistrationForm, UserLoginForm
from django.urls import reverse, reverse_lazy


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # delete old authorized user carts
                forgot_carts = Bascket.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user carts from anonimous session
                Bascket.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context
            

# def login(request):
#     if request.method == "POST":
#         form = User_loginform(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, вы вошли в аккаунт")

#                 if session_key:
#                     forgot_carts = Bascket.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Bascket.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page and redirect_page != reverse("user:logout"):
#                     return HttpResponseRedirect(
#                         request.POST.get("next")
#                     )  # редирект на нужную страницу после авторизации мы идём по указанной ссылке, а не как обычно на index

#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = User_loginform()

#     context = {
#         "title": "Home - Авторизация",
#         "form": form,
#     }

#     return render(request, "users/login.html", context)

class UserRegistrationForm(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Bascket.objects.filter(session_key=session_key).update(user=user)
            messages.success(
                self.request,
                f"{user.username}, вы успешно зарегистрировались и вошли в аккаунт",
            )
            return HttpResponseRedirect(self.success_url)
    
# def registration(request):

#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = request.session.session_key

#             user = form.instance
#             auth.login(request, user)

#             if session_key:
#                 Bascket.objects.filter(session_key=session_key).update(user=user)

#             messages.success(
#                 request,
#                 f"{user.username}, вы успешно зарегистрировались и вы вошли в аккаунт",
#             )
#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()
#     context = {
#         "title": "Home - Регистрация",
#         "form": form,
#     }

#     return render(request, "users/registration.html", context)

class UserProfilaView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = Profileform
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset = ...):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профель успещно обновлён")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home - Кабинет"
        context['orders'] = (
        Order.objects.filter(user=self.request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
        )
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, "Ошибка")
        return super().form_invalid(form)
    
# @login_required  # нужно для запрета анонимным пользователям открывать приложения не доступные без юзера
# def profile(request):

#     if request.method == "POST":
#         form = Profileform(
#             data=request.POST, instance=request.user, files=request.FILES
#         )

#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профель успещно обновлён")
#             return HttpResponseRedirect(reverse("user:profile"))
#     else:
#         form = Profileform(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )

#     context = {
#         "title": "Home - Регистрация",
#         "form": form,
#         'orders': orders,
#     }

#     return render(request, "users/profile.html", context)

class UserCartView(TemplateView):
    template_name = "users/users-cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context
# def users_cart(request):
#     return render(request, "users/users-cart.html")

#эту функцию мы оставляем, так как в новой версии джанго для logout использовать можн LogoutView(прямо в url, тут его не надо прописывать), но на него нкжно отсылать get запрос с csrf токеном
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))
