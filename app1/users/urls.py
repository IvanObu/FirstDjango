from users import views
from app import settings
from django.urls import include, path
from django.conf.urls.static import static
app_name = "users"  # для namespace

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationForm.as_view(), name="registration"),
    path("profile/", views.UserProfilaView.as_view(), name="profile"),
    path("logout/", views.logout, name="logout"),
    path("users-cart/", views.UserCartView.as_view(), name="users_cart"),
 #может преобразовывать числа в строки!!!, надо число поставить раньше
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)