from django.http import HttpResponse
from django.views.generic import (
    TemplateView,
    FormView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import HasCustomerAccessPermission
from order.models import UserAddressModel
from order.forms import CheckOutForm
from cart.models import CartModel, CartItemModel
from order.models import OrderModel, OrderItemModel
from django.urls import reverse_lazy
from cart.cart import CartSession
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import PaymentModel
from json.decoder import JSONDecodeError


class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('order:completed')

    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
       

        cart = CartModel.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calculate_total_price()
        order.total_price = total_price
        order.save()
        return redirect(self.create_payment_url(order))

    def create_payment_url(self, order):
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request(order.get_price())
      
        payment_obj = PaymentModel.objects.create(
            authority_id = response.get('data', {}).get('authority'),
            amount=order.get_price(),
        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(response.get('data', {}).get('authority'))

    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        
        context["cart_items"] = cart.cart_items.all()
        context["addresses"] = UserAddressModel.objects.filter(
            user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        return context


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/completed.html"
    
class OrderFailedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/failed.html"