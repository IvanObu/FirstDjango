from django.core import paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from goods.models import Products


# Create your views here.
def catalog(request, category_slug, page=1):
    
    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

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

    return render(request, "goods/product.html", context=context)
