from django import template

from bascket.models import Bascket

register = template.Library()

@register.simple_tag()
def user_bascket(request):
    if request.user.is_authenticated:
        return Bascket.objects.filter(user=request.user)