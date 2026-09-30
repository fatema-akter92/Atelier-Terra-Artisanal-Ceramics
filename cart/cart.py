from decimal import Decimal
from django.conf import settings
from products.models import Product
from atelier.models import CustomCreation, CeramicShape, GlazeOption


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                'items': {},
                'coupon': None,
                'discount_percent': 0
            }
        # In case old structure was just a dict
        if 'items' not in cart:
            old_items = cart
            cart = self.session[settings.CART_SESSION_ID] = {
                'items': old_items,
                'coupon': None,
                'discount_percent': 0
            }
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a regular catalog product to the cart."""
        item_key = f"prod_{product.id}"
        items = self.cart['items']
        if item_key not in items:
            items[item_key] = {
                'type': 'product',
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': 0,
                'image_url': product.image.url if product.image else '',
                'slug': product.slug,
                'category': product.category.name,
                'tagline': product.tagline,
            }
        if override_quantity:
            items[item_key]['quantity'] = quantity
        else:
            items[item_key]['quantity'] += quantity
        self.save()

    def add_custom(self, custom_creation_id, custom_obj=None, quantity=1):
        """Add an artisan custom studio piece to the cart."""
        if custom_obj is None:
            custom_obj = CustomCreation.objects.get(id=custom_creation_id)
        
        item_key = f"custom_{custom_obj.id}"
        items = self.cart['items']
        items[item_key] = {
            'type': 'custom',
            'custom_id': custom_obj.id,
            'name': f"Custom {custom_obj.shape.name}",
            'price': str(custom_obj.final_price),
            'quantity': quantity,
            'glaze_name': custom_obj.glaze.name,
            'glaze_color': custom_obj.glaze.hex_color,
            'finish_texture': custom_obj.finish_texture,
            'lamp_stand_color': custom_obj.get_lamp_stand_color_display() if hasattr(custom_obj, 'get_lamp_stand_color_display') else custom_obj.lamp_stand_color,
            'engraving_text': custom_obj.engraving_text,
            'preview_data_url': custom_obj.preview_data_url,
            'shape_name': custom_obj.shape.name,
        }
        self.save()

    def add_nook_bundle(self, product_ids):
        """Add multiple items from the Cozy Nook builder with an automatic bundle perk."""
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.add(product, quantity=1)
        self.apply_coupon('COZYNOOK15')
        self.save()

    def remove(self, item_key):
        """Remove an item by its unique key (e.g. prod_5 or custom_2)."""
        if item_key in self.cart['items']:
            del self.cart['items'][item_key]
            self.save()

    def update_quantity(self, item_key, quantity):
        if item_key in self.cart['items']:
            if quantity > 0:
                self.cart['items'][item_key]['quantity'] = quantity
            else:
                del self.cart['items'][item_key]
            self.save()

    def apply_coupon(self, code):
        code_upper = code.strip().upper()
        if code_upper == 'WARMTH10':
            self.cart['coupon'] = 'WARMTH10'
            self.cart['discount_percent'] = 10
            self.save()
            return True, "10% Warmth Discount Applied!"
        elif code_upper == 'COZYNOOK15':
            self.cart['coupon'] = 'COZYNOOK15'
            self.cart['discount_percent'] = 15
            self.save()
            return True, "15% Cozy Nook Bundle Discount Applied!"
        elif code_upper == 'ATELIER20':
            self.cart['coupon'] = 'ATELIER20'
            self.cart['discount_percent'] = 20
            self.save()
            return True, "20% Artisan VIP Discount Applied!"
        return False, "Invalid promotional code"

    def remove_coupon(self):
        self.cart['coupon'] = None
        self.cart['discount_percent'] = 0
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """Iterate over the items in the cart."""
        items = self.cart.get('items', {})
        for key, item in items.items():
            item_copy = item.copy()
            item_copy['key'] = key
            unit_price = Decimal(item['price'])
            item_copy['unit_price'] = unit_price
            item_copy['total_price'] = unit_price * item['quantity']
            yield item_copy

    def __len__(self):
        """Count all item quantities."""
        items = self.cart.get('items', {})
        return sum(item['quantity'] for item in items.values())

    def get_subtotal_price(self):
        items = self.cart.get('items', {})
        return sum(Decimal(item['price']) * item['quantity'] for item in items.values())

    def get_discount_amount(self):
        subtotal = self.get_subtotal_price()
        percent = self.cart.get('discount_percent', 0)
        if percent > 0:
            return round(subtotal * Decimal(percent) / Decimal(100), 2)
        return Decimal('0.00')

    def get_shipping_cost(self):
        subtotal = self.get_subtotal_price()
        if subtotal == 0:
            return Decimal('0.00')
        # Free shipping on orders over $150
        if subtotal >= Decimal('150.00'):
            return Decimal('0.00')
        return Decimal('12.00')

    def get_total_price(self):
        subtotal = self.get_subtotal_price()
        discount = self.get_discount_amount()
        shipping = self.get_shipping_cost()
        return max(Decimal('0.00'), subtotal - discount + shipping)

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {
            'items': {},
            'coupon': None,
            'discount_percent': 0
        }
        self.save()
