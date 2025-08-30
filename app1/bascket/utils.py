from django import template

from bascket.models import Bascket

def get_user_bascket(request):
    if request.user.is_authenticated:
        return Bascket.objects.filter(user=request.user).select_related('product') #inner join чобы был 1 sql запрос
    
    if not request.session.session_key:
        request.session.create()
    return Bascket.objects.filter(session_key=request.session.session_key).select_related('product')