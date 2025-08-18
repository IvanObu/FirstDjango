from django.urls import path
from goods import views

app_name = "goods"  # для namespace

urlpatterns = [
    path("<slug:category_slug>/", views.catalog, name="index"),
    path("search/", views.catalog, name="search"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("product/<slug:product_slug>/", views.product, name="product"), #может преобразовывать числа в строки!!!, надо число поставить раньше
]
