from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from product.models import ProductModel, ProductStatusType
from .cart import CartSession


class SessionAddProductView(View):
    def post(self, request, *args, **kwargs):
        # دریافت مقادیر از درخواست POST
        product_id = request.POST.get("product_id")
        color_id = request.POST.get("color_id")
        quantity = request.POST.get("quantity", 1)


        # بررسی صحت داده‌ها
        if product_id and ProductModel.objects.filter(id=product_id, status=ProductStatusType.publish.value).exists():
            # ایجاد یا دریافت سبد خرید
            cart = CartSession(request.session)
            # افزودن محصول به سبد خرید
            cart.add_product(product_id=product_id, color_id=color_id,quantity=int(quantity))

        # اگر کاربر وارد سیستم شده باشد، سینک با پایگاه داده انجام می‌شود
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        # ارسال پاسخ JSON با جزئیات سبد خرید و تعداد کل محصولات
        return JsonResponse({
            "cart": cart.get_cart_dict(),
            "total_quantity": cart.get_total_quantity()
        })

class CartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        context["total_original_price"] = cart.get_total_original_amount()  # قیمت کل قبل از تخفیف
        return context
    
class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        color_id = request.POST.get("color_id")  # دریافت رنگ محصول        
        if product_id:
            cart.remove_product(product_id, color_id=color_id)

        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})
    

    
class SessionUpdateProductQuantityView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        color_id = request.POST.get("color_id")
        

        if product_id and quantity:
            cart.update_product_quantity(product_id, color_id,quantity)

        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})