from django.urls import path
from users import views

app_name = "users"  # для namespace

urlpatterns = [
    path("", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("users-cart/", views.users_cart, name="users_cart"),
 #может преобразовывать числа в строки!!!, надо число поставить раньше
]
