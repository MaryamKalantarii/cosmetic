from django.contrib import admin
from .models import ReviewModel

# Register your models here.

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rating","status", "created_date")
    def rating_stars(self, obj):
        return "⭐" * obj.rating  # نمایش امتیاز به‌صورت ستاره
    rating_stars.short_description = "امتیاز"