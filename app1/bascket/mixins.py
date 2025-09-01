from django.template.loader import render_to_string
from django.urls import reverse
from bascket.models import Bascket
from bascket.utils import get_user_bascket


class BascketMixin:
    
    def get_bascket(self, request, product=None, bascket_id=None):

        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product

        if bascket_id:
            query_kwargs["id"] = bascket_id

        return Bascket.objects.filter(**query_kwargs).first()
    
    def render_bascket(self, request):
        user_cart = get_user_bascket(request)
        context = {"bascket": user_cart}

        # if referer page is create_order add key orders: True to context
        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True
        return render_to_string("bascket/includes/included_bascket.html", context, request=request)