from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from bascket.mixins import BascketMixin
from bascket.models import Bascket
from bascket.utils import get_user_bascket
from goods.models import Products
from django.urls import reverse

# Create your views here.


class BascketAddView(BascketMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)

        bascket = self.get_bascket(request, product=product)

        if bascket:
            bascket.quantity += 1
            bascket.save()
        else:
            Bascket.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key= request.session.session_key if not request.user.is_authenticated else None,
                product=product,
                quantity=1,
            )
        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": self.render_bascket(request),
        }
        return JsonResponse(response_data)
# def bascket_add(request):

#     product_id = request.POST.get("product_id")

#     product = Products.objects.get(id=product_id)

#     if request.user.is_authenticated:
#         bascket = Bascket.objects.filter(user=request.user, product=product)

#         if bascket.exists():
#             bascket = bascket.first()
#             if bascket:
#                 bascket.quantity += 1
#                 bascket.save()

#         else:
#             Bascket.objects.create(user=request.user, product=product, quantity=1)
#     else:
#         bascket = Bascket.objects.filter(
#             session_key=request.session.session_key, product=product
#         )
#         if bascket.exists():
#             bascket = bascket.first()
#             if bascket:
#                 bascket.quantity += 1
#                 bascket.save()

#         else:
#             Bascket.objects.create(
#                 session_key=request.session.session_key, product=product, quantity=1
#             )

#     # return redirect(request.META['HTTP_REFERER'])
#     user_bascket = get_user_bascket(request)
#     cart_items_html = render_to_string(
#         "bascket/includes/included_bascket.html",
#         {"bascket": user_bascket},
#         request=request,
#     )

#     response_data = {
#         "message": "Товар добавлен в корзину",
#         "cart_items_html": cart_items_html,
#     }

#     return JsonResponse(response_data)

class BascketChangeView(BascketMixin, View):
    def post(self, request):
        bascket_id = request.POST.get("cart_id")
        bascket = self.get_bascket(request, bascket_id=bascket_id)
        bascket.quantity = request.POST.get('quantity')
        bascket.save()
        quantity = bascket.quantity
        response_data = {
            "message": "Товар добавлен в корзину",
            "quantity":quantity,
            "cart_items_html": self.render_bascket(request),
        }
        return JsonResponse(response_data)
    
# def bascket_change(request):
#     bascket_id = request.POST.get("cart_id")  # получаем cart_id
#     quantity = request.POST.get("quantity")  # уже получили поменянное значение после js

#     bascket = Bascket.objects.get(id=bascket_id)
#     bascket.quantity = quantity
#     bascket.save()

#     user_bascket = get_user_bascket(request)

#     context = {"bascket": user_bascket}

#     # if referer page is create_order add key orders: True to context

#     referer = request.META.get("HTTP_REFERER", "")
#     if reverse("orders:create_order") in referer:
#         context["order"] = True
#     else:
#         context["order"] = False  # Явно устанавливаем False

#     cart_items_html = render_to_string(
#         "bascket/includes/included_bascket.html", context, request=request
#     )

#     response_data = {
#         "message": "Количество изменено",
#         "cart_items_html": cart_items_html,
#         "quantity_deleted": quantity,
#     }
#     print(context)

#     return JsonResponse(response_data)

class BascketRemoveView(BascketMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        
        cart = self.get_bascket(request, bascket_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            'cart_items_html': self.render_bascket(request)
        }

        return JsonResponse(response_data)
    
# def bascket_remove(request):

#     bascket_id = request.POST.get("cart_id")  # получаем cart_id
#     bascket = Bascket.objects.get(id=bascket_id)
#     quantity = bascket.quantity
#     bascket.delete()

#     user_cart = get_user_bascket(request)

#     context = {"bascket": user_cart}

#     referer = request.META.get("HTTP_REFERER", "")
#     if reverse("orders:create_order") in referer:
#         context["order"] = True
#     else:
#         context["order"] = False  # Явно устанавливаем False

#     cart_items_html = render_to_string(
#         "bascket/includes/included_bascket.html", context, request=request
#     )

#     response_data = {
#         "message": "Товар удален",
#         "cart_items_html": cart_items_html,
#         "quantity_deleted": quantity,
#     }

#     return JsonResponse(response_data)
