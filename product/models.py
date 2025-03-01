from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


class ProductStatusType(models.IntegerChoices):
    publish = 1 , ("نمایش")
    draft = 2 , ("عدم نمایش")


class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
 
    def __str__(self):
        return self.title
    

class ColorModel(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, null=True, blank=True)  # برای کد رنگ مثل #FFFFFF

    def __str__(self):
        return self.name
    



class ProductModel(models.Model):
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField()
    colors = models.ManyToManyField(ColorModel, blank=True)
    avg_rate = models.FloatField(default=0.0) # امتیاز
    image1 = models.ImageField(upload_to='product')
    image2 = models.ImageField(upload_to='product', null=True ,blank=True)
   
    
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices,default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=0)
    discount_percent = models.IntegerField(default=0,validators = [MinValueValidator(0),MaxValueValidator(100)])
    views = models.PositiveIntegerField(default=0)  # تعداد بازدید

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        
    def __str__(self):
        return self.title
    
    def get_price(self):        
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discounted_amount = self.price - discount_amount
        return round(discounted_amount)
    
    def is_discounted(self):
        return self.discount_percent != 0
    
    def is_published(self):
        return self.status == ProductStatusType.publish.value

    @property
    def is_out_of_stock(self):
        return self.stock == 0

class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.CustomeUser",on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title