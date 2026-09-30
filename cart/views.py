from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override') == 'True'
    
    cart.add(product=product, quantity=quantity, override_quantity=override)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to your cart!",
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })

    messages.success(request, f"Added '{product.name}' to your cart.")
    return redirect('cart:cart_detail')


def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    messages.info(request, "Item removed from your cart.")
    return redirect('cart:cart_detail')


@require_POST
def cart_update_quantity(request, item_key):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update_quantity(item_key, quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal_price()),
            'cart_discount': str(cart.get_discount_amount()),
            'cart_shipping': str(cart.get_shipping_cost()),
            'cart_total': str(cart.get_total_price())
        })

    return redirect('cart:cart_detail')


@require_POST
def apply_coupon(request):
    cart = Cart(request)
    code = request.POST.get('code', '')
    success, msg = cart.apply_coupon(code)
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect('cart:cart_detail')


def remove_coupon(request):
    cart = Cart(request)
    cart.remove_coupon()
    messages.info(request, "Promotional code removed.")
    return redirect('cart:cart_detail')
