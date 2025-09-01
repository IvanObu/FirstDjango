from django.views.generic import DetailView, ListView
from goods.models import Products
from goods.utils import q_search
from django.http import Http404


# Create your views here.
# def catalog(request, category_slug=None):
    
#     page = int(request.GET.get('page', 1))
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)

#     if category_slug == "vse-tovary":
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#     if order_by and order_by != 'default':
#         goods = goods.order_by(order_by)

#     pag = paginator.Paginator(goods, 3)
#     current_page = pag.page(page)
    
#     context = {
#         "home": "Home - каталог",
#         "goods": current_page,
#         "slug_url": category_slug,
#     }
#     return render(request, "goods/catalog.html", context)

class CatalogView(ListView):
    model = Products
    template_name = "goods/catalog.html"
    context_object_name = 'goods' # переопределение имени, которое по умолчанию делает джанго
    paginate_by = 3 # количество товаров

    allow_empty = False 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Каталог'
        context['slug_url'] = self.kwargs.get('category_slug')
        return context

    def get_queryset(self):
        category_slug=self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if category_slug == "vse-tovary":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
        if on_sale:
            goods = goods.filter(discount__gt=0)
        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

# def product(request, product_slug=False, product_id=False):

#     if product_slug:
#         product = Products.objects.get(slug=product_slug)
#     else:
#         product = Products.objects.get(id=product_id)
#     context = {
#         "product": product
#     }

#     return render(request, "goods/product.html", context)


class ProductView(DetailView):

    # model = Products это отображает все о нашем продукте Products.objects меняется на super().get_queryset()
    # slug_field = 'slug'
    slug_url_kwarg = 'product_slug' #получаем slug из конвектора url
    template_name = "goods/product.html"
    context_object_name = 'product' # переопределение имени, которое по умолчанию делает джанго
    def get_object(self, queryset = ...):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context