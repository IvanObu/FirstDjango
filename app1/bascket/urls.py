from django.urls import path
from bascket import views

app_name = "bascket"  # для namespace

urlpatterns = [
    path("bascket_add/", views.BascketAddView.as_view(), name="bascket_add"),
    path("bascket_change/", views.BascketChangeView.as_view(), name="bascket_change"),
    path("bascket_remove/", views.BascketRemoveView.as_view(), name="bascket_remove"),
]
