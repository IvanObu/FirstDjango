from django.urls import path
from main import views
app_name = 'main' #для namespace
urlpatterns = [
    path ('', views.IndexView.as_view(), name='index'),
    path ('about/', views.AboutView.as_view(), name='about'),
]
