from django.db import models

# Create your models here.

class CartModel(models.Model):
    user = models.ForeignKey("accounts.CustomeUser",on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    
    def calculate_total_price(self):
        return sum(item.product.get_price() * item.quantity for item in self.cart_items.all())
        
    
class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="cart_items") 
    product = models.ForeignKey('product.ProductModel', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    color = models.ForeignKey('product.ColorModel', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def multiply_by_number(self):
        return self.quantity * self.product.get_price()
    def __str__(self):
        return f"{self.product.title} - {self.cart.id} - {self.color}"

    

    