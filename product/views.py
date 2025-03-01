from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView,View
from product.models import ProductModel,ProductStatusType,ProductCategoryModel,WishlistProductModel
from django.shortcuts import render
from django.core.exceptions import FieldError
from review.models import ReviewModel, ReviewStatusType 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q

class ProductGridView(ListView):
    template_name = 'product/product-grid.html'
    paginate_by = 12

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset =ProductModel.objects.filter(
            status=ProductStatusType.publish.value)
        
        #search
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(
                Q(title__icontains=search_q) | Q(brief_description__icontains=search_q) | Q(description__icontains=search_q))
    
         # فیلتر بر اساس کتگوری
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        sort_option = self.request.GET.get("sort")
        if sort_option == "cheapest":
            queryset = queryset.order_by('price')  
        elif sort_option == "most_expensive":
            queryset = queryset.order_by('-price')  
        elif sort_option == "newest":
            queryset = queryset.order_by('-created_date')  
        elif sort_option == "oldest":
            queryset = queryset.order_by('created_date')  
        
        return queryset
  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =ProductCategoryModel.objects.all()  # ارسال لیست همه کتگوری‌ها به تمپلیت
        context['selected_category'] = self.request.GET.get('category')
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list(
            "product__id", flat=True) if self.request.user.is_authenticated else []
        return context



class ProductDetailView(DetailView):
    template_name = 'product/product-detail.html'
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        # افزایش تعداد بازدید
        product.views += 1
        product.save(update_fields=['views'])
        # فیلتر کردن نظرات تایید شده مربوط به این محصول
        context['reviews'] = ReviewModel.objects.filter(
            product=product,
            status=ReviewStatusType.accepted.value
        ).order_by('-created_date')  # اگر می‌خواهید نظرات به ترتیب تاریخ نزولی نمایش داده شوند
        context["wishlist_items"] = WishlistProductModel.objects.filter(user=self.request.user).values_list(
            "product__id", flat=True) if self.request.user.is_authenticated else []
        return context


class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(
                    user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(
                    user=request.user, product_id=product_id)
                message = "محصول به لیست علایق اضافه شد"

        return JsonResponse({"message": message})
    