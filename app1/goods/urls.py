from django.urls import path
from goods import views

app_name = "goods"  # для namespace

urlpatterns = [
    path("<slug:category_slug>/", views.CatalogView.as_view(), name="index"),
    path("search/", views.CatalogView.as_view(), name="search"),
    # path("product/<int:product_id>/", views.product, name="product"),
    path("product/<slug:product_slug>/", views.ProductView.as_view(), name='product'), #может преобразовывать числа в строки!!!, надо число поставить раньше
]
