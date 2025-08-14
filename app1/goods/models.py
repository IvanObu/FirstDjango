from tabnanny import verbose
from unicodedata import category
from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категорию'
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"

class Products(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', null=True, blank=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places = 2, verbose_name = 'Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places = 2, verbose_name = 'Скидка в %')
    quality = models.PositiveBigIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    
    class Meta:
        db_table = 'Product'
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Количество - {self.name}"
    

    def display_id(self):
        return f'{self.id:05}'
    

    def self_price(self):

        if self.discount:
            return round(self.price*(1-self.discount/100),2)
        
        return self.price
