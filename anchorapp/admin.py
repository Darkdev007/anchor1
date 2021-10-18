from django.contrib import admin
from .models import Category,Product,ShopCart

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','image')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','image','min_quant','max_quant','best_seller','latest','available')
    list_display_links = ('id','title',)
    list_per_page = 25
    list_editable = ('best_seller','latest','available')

class ShopCartAdmin(admin.ModelAdmin):
    list_display= ('id','user','product','quantity','paid_item','cart_no')
    list_per_page = 25

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ShopCart,ShopCartAdmin)

