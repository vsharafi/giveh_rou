from .models import Product
from django.contrib import messages
from django.utils.translation import gettext as _

class Cart:
    def __init__(self, request):

        """
        Initialize the cart
        """

        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, size, color, quantity=1, replace_current_quantity=False):

        """
        Add a product to the cart
        """
        cart_item = '1'
        flag = True
        for item in self.cart.items():
            if item[1]['product_id'] == product.id and item[1]['size'] == size and item[1]['color'] == color:
                if replace_current_quantity:
                     item[1]['quantity'] = quantity
                     messages.success(self.request, _('Product quantity of cart has successfully updated '))
                else:
                    item[1]['quantity'] += quantity
                    messages.success(self.request, _('Product successfully added to cart.'))

                flag = False

        keys = list(self.cart.keys())
        if flag:
            while flag:
                if cart_item in keys:
                    cart_item = str(int(cart_item) + 1)
                    continue
                flag = False
                
            self.cart[cart_item] = {'product_id': product.id}
            self.cart[cart_item]['size'] = size
            self.cart[cart_item]['color'] = color
            self.cart[cart_item]['quantity'] = quantity

            messages.success(self.request, _('Product successfully added to cart.'))
        self.save()

    def remove(self, cart_item):
        cart_item = str(cart_item)
                
        """
        Remove a product from the cart
        """
        if cart_item in self.cart.keys():
            del self.cart[cart_item]
            messages.success(self.request, _("Product successfully removed from cart."))
            self.save()
        
    def save(self):

        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        product_ids = [value['product_id'] for value in self.cart.values()]
        cart = self.cart.copy()
        keys = list(cart.keys())
        for index,id in enumerate(product_ids):
            cart[str(keys[index])]['product_obj'] = Product.objects.get(id=id)
            cart[str(keys[index])]['cart_item'] = keys[index]


        
        for item in cart.values():
            item['total_price'] = item['product_obj'].new_price * item['quantity']
            item['total_discount'] = item['product_obj'].discount_amount * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart)
    
    def clear(self):
        del self.session['cart']
        messages.success(self.request, _("All product successfully removed from cart."))
        self.save()

    def get_total_price(self):
        return sum(item['product_obj'].price * item['quantity'] for item in self.cart.values())
    
    def get_new_total_price(self):
        return sum(item['product_obj'].new_price * item['quantity'] for item in self.cart.values())
    
    def total_discout_amount(self):
        return sum(item['product_obj'].discount_amount * item['quantity'] for item in self.cart.values())

