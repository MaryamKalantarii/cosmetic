from django.db import models
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import ProductColorStock

class OrderStatusType(models.IntegerChoices):
    pending = 1 , "در انتظار پرداخت"
    success = 2, "موفقیت آمیز"
    failed = 3,"لغو شده"

class UserAddressModel(models.Model):
    user = models.ForeignKey('accounts.CustomeUser',on_delete=models.CASCADE)
    
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


# Create your models here.
class OrderModel(models.Model):
    user = models.ForeignKey('accounts.CustomeUser',on_delete=models.PROTECT)
    
    # order address information
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    payment = models.ForeignKey('payment.PaymentModel',on_delete=models.SET_NULL,null=True,blank=True)
    total_price = models.DecimalField(default=0,max_digits=10,decimal_places=0)

    status = models.IntegerField(choices=OrderStatusType.choices,default=OrderStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
    
    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())
    
    def __str__(self):
        return f"{self.user.email} - {self.id}"
    
    def get_status(self):
        return {
            "id":self.status,
            "title":OrderStatusType(self.status).name,
            "label":OrderStatusType(self.status).label,
        }
        
    def get_full_address(self):
        return f"{self.state},{self.city},{self.address}"
    
    @property
    def is_successful(self):
        return self.status == OrderStatusType.success.value
    
    def get_price(self):
        return self.total_price
    
    
class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel,on_delete=models.CASCADE,related_name="order_items") 
    product = models.ForeignKey('product.ProductModel',on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=0)
    color = models.ForeignKey('product.ColorModel', on_delete=models.PROTECT, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.title} - {self.order.id}"
    



@receiver(post_save, sender=OrderModel)
def reduce_stock(sender, instance, **kwargs):
    """ کاهش موجودی محصول و رنگ بعد از پرداخت موفق """
    if instance.is_successful:  # فقط در صورتی که پرداخت موفق باشد
        for order_item in instance.order_items.all():
            product = order_item.product
            quantity = order_item.quantity

            # کم کردن موجودی کلی محصول
            if product.stock >= quantity:
                product.stock -= quantity
                product.save(update_fields=['stock'])
            else:
                raise ValueError(f"موجودی کافی برای {product.title} وجود ندارد!")

            # کم کردن موجودی رنگ محصول، اگر رنگی انتخاب شده باشد
            if order_item.color:
                product_color_stock = ProductColorStock.objects.filter(
                    product=product, color=order_item.color
                ).first()
                
                if product_color_stock:
                    if product_color_stock.stock >= quantity:
                        product_color_stock.stock -= quantity
                        product_color_stock.save(update_fields=['stock'])
                    else:
                        raise ValueError(f"موجودی کافی برای رنگ {order_item.color.name} از {product.title} وجود ندارد!")
