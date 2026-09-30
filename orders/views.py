from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from products.models import Product


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your shopping basket is empty.")
        return redirect('products:product_list')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data.update({
                'phone': profile.phone,
                'address_line1': profile.street_address,
                'city': profile.city,
                'state': profile.state,
                'postal_code': profile.postal_code,
                'country': profile.country or 'United States',
            })

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            # Financials
            subtotal = cart.get_subtotal_price()
            discount = cart.get_discount_amount()
            shipping_method = form.cleaned_data['shipping_method']
            
            if shipping_method == 'fragile_white_glove':
                shipping_cost = Decimal('25.00')
            else:
                shipping_cost = cart.get_shipping_cost()

            order.subtotal = subtotal
            order.discount_amount = discount
            order.shipping_cost = shipping_cost
            order.total_price = subtotal - discount + shipping_cost
            order.coupon_code = cart.cart.get('coupon')
            order.save()

            # Create order items
            for item in cart:
                product_instance = None
                if item.get('type') == 'product':
                    try:
                        product_instance = Product.objects.get(id=item['product_id'])
                        if product_instance.stock >= item['quantity']:
                            product_instance.stock -= item['quantity']
                            product_instance.save()
                    except Product.DoesNotExist:
                        pass
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product_instance,
                        item_type='product',
                        item_name=item['name'],
                        price=item['unit_price'],
                        quantity=item['quantity']
                    )
                else:
                    # Custom creation piece
                    details = (
                        f"Shape: {item.get('shape_name')}\n"
                        f"Glaze: {item.get('glaze_name')} ({item.get('glaze_color')})\n"
                        f"Texture: {item.get('finish_texture')}\n"
                        f"Stand/Hardware: {item.get('lamp_stand_color')}\n"
                        f"Engraving Stamp: {item.get('engraving_text') or 'None'}"
                    )
                    OrderItem.objects.create(
                        order=order,
                        item_type='custom',
                        item_name=item['name'],
                        price=item['unit_price'],
                        quantity=item['quantity'],
                        custom_details=details,
                        preview_data_url=item.get('preview_data_url', '')
                    )

            # Clear cart
            cart.clear()
            messages.success(request, f"Order #{order.order_number} confirmed! Our artisans are preparing your pieces.")
            return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        form = OrderCreateForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/confirmation.html', {'order': order})


def track_order(request):
    order = None
    searched = False
    order_number = request.GET.get('order_number', '').strip()
    email = request.GET.get('email', '').strip()

    if order_number and email:
        searched = True
        try:
            order = Order.objects.get(order_number__iexact=order_number, email__iexact=email)
        except Order.DoesNotExist:
            order = None

    context = {
        'order': order,
        'searched': searched,
        'order_number': order_number,
        'email': email,
    }
    return render(request, 'orders/tracking.html', context)
