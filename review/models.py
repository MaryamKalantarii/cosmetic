from django.db import models
from product.models import ProductModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django.conf import settings
# Create your models here.


class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"




class ReviewModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('product.ProductModel', on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.IntegerField(choices=[(i, f"{i} ستاره") for i in range(1, 6)], default=5)
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_date"]
    
    def __str__(self):
        return f"{self.user} - {self.product.id}"
    
    
    def get_status(self):
        return {
            "id":self.status,
            "title":ReviewStatusType(self.status).name,
            "label":ReviewStatusType(self.status).label,
        }
        
        
@receiver(post_save,sender=ReviewModel)
def calculate_avg_review(sender,instance,created,**kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        average_rating = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted).aggregate(Avg('rating'))['rating__avg']
        product.avg_rate = round(average_rating,1)
        product.save()