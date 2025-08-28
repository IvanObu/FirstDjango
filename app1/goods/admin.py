from django.contrib import admin
from goods.models import Categories, Products
# Register your models here.


# admin.site.register(Categories)


# admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = [ 'name',]

@admin.register(Products) 
class ProductssAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = [ 'name', 'quantity', 'price', 'discount'] #теперь не str метод
    list_editable = ['discount',]
    search_fields = ['name', 'description']
    list_filter = ["discount", 'quantity', 'category']
    #поля в описании товаров
    fields =  [
        'name',
        'category',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'quantity',
    ]