from django.urls import path
from bascket import views

app_name = "bascket"  # для namespace

urlpatterns = [
    path("bascket_add/<slug:product_slug>", views.bascket_add, name="bascket_add"),
    path("bascket_change/<slug:product_slug>", views.bascket_change, name="bascket_change"),
    path("bascket_remove/<slug:product_slug>", views.bascket_remove, name="bascket_remove"),
]
