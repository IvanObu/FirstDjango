from django.core import paginator
from django.shortcuts import get_list_or_404 , render
from goods.models import Products
from goods.utils import q_search
from django.http import Http404
from django.shortcuts import render

# Create your views here.
def catalog(request, category_slug=None):
    
    page = int(request.GET.get('page', 1))
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404()
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    pag = paginator.Paginator(goods, 3)
    current_page = pag.page(page)
    
    context = {
        "home": "Home - каталог",
        "goods": current_page,
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug=False, product_id=False):

    if product_slug:
        product = Products.objects.get(slug=product_slug)
    else:
        product = Products.objects.get(id=product_id)
    context = {
        "product": product
    }

    return render(request, "goods/product.html", context)
