import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import CeramicShape, GlazeOption, CustomCreation
from products.models import Product
from cart.cart import Cart


def atelier_studio(request):
    """Interactive Custom Ceramic Atelier Studio"""
    shapes = CeramicShape.objects.filter(is_active=True)
    glazes = GlazeOption.objects.filter(is_active=True)
    
    selected_shape_id = request.GET.get('shape')
    initial_shape = None
    if selected_shape_id:
        try:
            initial_shape = shapes.get(id=selected_shape_id)
        except CeramicShape.DoesNotExist:
            initial_shape = shapes.first()
    else:
        initial_shape = shapes.first()

    context = {
        'shapes': shapes,
        'glazes': glazes,
        'initial_shape': initial_shape,
    }
    return render(request, 'atelier/studio.html', context)


@require_POST
def create_custom_ceramic(request):
    """Save custom creation and add to shopping cart"""
    shape_id = request.POST.get('shape_id')
    glaze_id = request.POST.get('glaze_id')
    finish_texture = request.POST.get('finish_texture', 'speckled')
    lamp_stand_color = request.POST.get('lamp_stand_color', 'white')
    engraving_text = request.POST.get('engraving_text', '').strip()[:30]
    preview_data_url = request.POST.get('preview_data_url', '')

    shape = get_object_or_404(CeramicShape, id=shape_id)
    glaze = get_object_or_404(GlazeOption, id=glaze_id)

    # Base price + glaze modifier + engraving fee
    final_price = shape.base_price + glaze.price_modifier
    if engraving_text:
        final_price += Decimal('8.00')

    if not request.session.session_key:
        request.session.create()

    custom_creation = CustomCreation.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        shape=shape,
        glaze=glaze,
        finish_texture=finish_texture,
        lamp_stand_color=lamp_stand_color,
        engraving_text=engraving_text,
        preview_data_url=preview_data_url,
        final_price=final_price,
    )

    # Add to cart
    cart = Cart(request)
    cart.add_custom(custom_creation.id, custom_obj=custom_creation, quantity=1)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added your custom {shape.name} to the cart!",
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })

    messages.success(request, f"Your custom handcrafted '{shape.name}' was added to your cart!")
    return redirect('cart:cart_detail')


def cozy_nook_builder(request):
    """
    Unique Feature: 'Style My Cozy Nook' Virtual Room & Desk Styler
    Modeled precisely after the aesthetic photo:
    Exposed off-white brick wall, light oak desk, pleated lamp, bud vase with flora, ceramic desk cup, and wallmates.
    """
    nook_products = Product.objects.filter(is_available=True)
    
    lamps = nook_products.filter(category__slug='ambient-lighting')
    vases = nook_products.filter(category__slug='artisanal-vases')
    desk_decor = nook_products.filter(category__slug='desk-decor')
    wallmates = nook_products.filter(category__slug='wallmates-fiber-art')
    ceramics = nook_products.filter(category__slug='ceramics-tableware')

    context = {
        'lamps': lamps,
        'vases': vases,
        'desk_decor': desk_decor,
        'wallmates': wallmates,
        'ceramics': ceramics,
        'all_nook_items': nook_products.filter(is_nook_hero=True),
    }
    return render(request, 'atelier/cozy_nook_builder.html', context)


@require_POST
def add_nook_bundle_to_cart(request):
    """Add selected items from the Cozy Nook builder with automatic bundle discount"""
    product_ids_raw = request.POST.get('product_ids', '[]')
    try:
        product_ids = json.loads(product_ids_raw)
    except json.JSONDecodeError:
        product_ids = [int(p) for p in request.POST.getlist('product_ids[]') if p.isdigit()]

    if not product_ids:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Please place at least one item on the desk!'})
        messages.warning(request, "Please style your nook with at least one item.")
        return redirect('atelier:cozy_nook_builder')

    cart = Cart(request)
    cart.add_nook_bundle(product_ids)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added your curated Cozy Nook look to the cart with a 15% discount!",
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })

    messages.success(request, "Your curated Cozy Nook room look was added to your cart with a 15% bundle discount!")
    return redirect('cart:cart_detail')
