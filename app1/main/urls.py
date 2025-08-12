from django.urls import path
from main import views
app_name = 'main' #для namespace
urlpatterns = [
    path ('', views.index, name='index'),
    path ('about/', views.about, name='about'),
]
