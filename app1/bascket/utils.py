from django import template

from bascket.models import Bascket

def get_user_bascket(request):
    if request.user.is_authenticated:
        return Bascket.objects.filter(user=request.user)