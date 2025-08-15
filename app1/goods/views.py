from django.shortcuts import get_object_or_404, render
from goods.models import Products


# Create your views here.
def catalog(request, category_slug):
    
    if category_slug == "vse-tovary":
        goods = Products.objects.all()
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    context = {
        "home": "Home - каталог",
        "goods": goods,
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
