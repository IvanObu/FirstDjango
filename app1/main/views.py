from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title':'Home',
        'content': 'Главная cраница магазина - Home'
    }
    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('прив броске')
