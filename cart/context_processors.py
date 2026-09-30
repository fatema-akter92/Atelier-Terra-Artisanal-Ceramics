from .cart import Cart


def cart(request):
    cart_obj = Cart(request)
    return {
        'cart': cart_obj,
        'cart_item_count': len(cart_obj),
        'cart_subtotal': cart_obj.get_subtotal_price(),
        'cart_total': cart_obj.get_total_price(),
        'cart_discount': cart_obj.get_discount_amount(),
        'cart_shipping': cart_obj.get_shipping_cost(),
    }
