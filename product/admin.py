from django.contrib import admin
from .models import ProductModel, ProductCategoryModel,WishlistProductModel,ColorModel

# Register your models here.

admin.site.register(ProductModel)
admin.site.register(ProductCategoryModel)
admin.site.register(ColorModel)



@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")