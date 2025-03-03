from product.models import ProductModel,ProductStatusType,ColorModel
from cart.models import CartModel,CartItemModel

class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def update_product_quantity(self, product_id, color_id=None,quantity=1):
        for item in self._cart["items"]:
            if (item["product_id"] == product_id and 
                item.get("color_id") == color_id):
                item["quantity"] = int(quantity)
                break
        self.save()
    
    def remove_product(self, product_id, color_id=None):
        for item in self._cart["items"]:
            if product_id == item["product_id"] and item.get("color_id") == color_id:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()
        
    def add_product(self, product_id, color_id=None,quantity=1):
        # جستجو برای محصول در سبد خرید
        for item in self._cart["items"]:
            if product_id == item["product_id"] and item.get("color_id") == color_id:
                item["quantity"] += 1  # اگر محصول قبلاً موجود بود، تعداد را افزایش می‌دهیم
                break
        else:
            # اگر محصول جدید است، آن را اضافه می‌کنیم
            new_item = {
                "product_id": product_id,
                "color_id": color_id,
                "quantity": int(quantity),
            }

            self._cart["items"].append(new_item)

        self.save()

    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def get_cart_dict(self):
        return self._cart

    def get_cart_items(self):
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            color_obj = None
           
            
            # بررسی وجود رنگ و استایل
            if item.get("color_id"):
                color_obj = ColorModel.objects.get(id=item["color_id"])
           

            item.update({
                "product_obj": product_obj,
                "color_obj": color_obj,
                "total_price": item["quantity"] * product_obj.get_price(),
            })
            print(f"Processed Item: {item}")
        return self._cart["items"]

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])

    def save(self):
        self.session.modified = True


    def sync_cart_items_from_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if (
                    str(cart_item.product.id) == item["product_id"]
                    and str(cart_item.color.id) == item.get("color_id")
                    
                ):
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {
                    "product_id": str(cart_item.product.id),
                    "quantity": cart_item.quantity,
                    "color_id": str(cart_item.color.id) if cart_item.color else None,
                    
                }
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()
            
        
    def merge_session_cart_in_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)
        
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            color_obj = None
            
            
            if item.get("color_id"):
                color_obj = ColorModel.objects.get(id=item["color_id"])
           

            cart_item, created = CartItemModel.objects.get_or_create(
                cart=cart,
                product=product_obj,
                color=color_obj,
               
            )
            cart_item.quantity = item["quantity"]
            cart_item.save()
            print(f"Synced CartItem to DB: {cart_item}") 
        session_product_ids = [item["product_id"] for item in self._cart["items"]]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()
            

        