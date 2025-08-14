from re import M
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from goods.models import Categories

# Create your views here.
def index(request):
    
    context = {
        'title':'Home - Глфвная',
        'content': "Магазин мебели HOME",
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title':'Home - О нас',
        'content': "О нас",
        'text_on_page': "Магазин очень классынй !!!"
    }
    return render(request, 'main/about.html', context)