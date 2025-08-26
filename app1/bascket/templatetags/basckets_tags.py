from django import template

from bascket.models import Bascket
from bascket.utils import get_user_bascket

register = template.Library()

@register.simple_tag()
def user_bascket(request):
    return get_user_bascket(request)