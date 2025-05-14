from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, size=None, color=None, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        key = f"{product_id}_{size}_{color}" if size and color else product_id
        
        if key not in self.cart:
            self.cart[key] = {
                'quantity': 0, 
                'price': str(product.discount_price if product.discount_price else product.price),
                'product_id': product_id
            }
            if size:
                self.cart[key]['size'] = size
            if color:
                self.cart[key]['color'] = color
        
        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    
    def remove(self, product, size=None, color=None):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        key = f"{product_id}_{size}_{color}" if size and color else product_id
        
        if key in self.cart:
            del self.cart[key]
            self.save()
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            for key, item in cart.items():
                if item['product_id'] == str(product.id):
                    item['product'] = product
                    item['price'] = Decimal(item['price'])
                    item['total_price'] = item['price'] * item['quantity']
                    yield {**item, 'key': key}
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()