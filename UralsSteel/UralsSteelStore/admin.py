from django.contrib import admin
from .models import *


# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'slug', 'description', 'price', 'is_published',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Products)
admin.site.register(Category_mp)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Category)
admin.site.register(Gallery)


@admin.register(Orders)
class OredersAdmin(admin.ModelAdmin):
    list_display = ('orders_id', 'id_of_products', 'customer_name', 'customer_phone_number', 'user')
