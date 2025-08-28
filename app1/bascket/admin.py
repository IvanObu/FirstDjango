from django.contrib import admin
from bascket.models import Bascket
# Register your models here.
class BascketTabAdmin(admin.TabularInline):
    model = Bascket
    fields = 'product','quantity', 'created_timestamp'
    search_fields = 'product','quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp',)
    extra = 1

@admin.register(Bascket)
class BascketAdmin(admin.ModelAdmin):
    list_display = [ 'user_display','product_display','quantity', 'created_timestamp', ]
    list_filter = [ 'created_timestamp','user','product__name', ]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)
