from django.contrib import admin
from .models import OrderModel, OrderItemModel, UserAddressModel

# Register your models here.


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "status",
        "created_date"
    )


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_date"
    )


    
@admin.register(UserAddressModel)
class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "state",
        "city",
        "zip_code",
        "created_date"
    )