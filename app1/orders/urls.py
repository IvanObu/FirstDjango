from django.urls import path
from orders import views

app_name = "orders"  # для namespace

urlpatterns = [
    path("create_order/", views.create_order, name="create_order"),
]