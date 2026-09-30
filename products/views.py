from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review
from accounts.models import Wishlist


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search filter
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tagline__icontains=query) |
            Q(material__icontains=query)
        )

    # Sort filter
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'bestseller':
        products = products.order_by('-is_bestseller', '-created_at')
    else:
        products = products.order_by('-is_featured', '-created_at')

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'current_sort': sort,
        'total_count': products.count(),
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    is_wishlisted = False
    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(user=request.user, product=product).exists()

    reviews = product.reviews.filter(is_approved=True)

    context = {
        'product': product,
        'related_products': related_products,
        'is_wishlisted': is_wishlisted,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)


def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        name = request.POST.get('name', 'Artisan Collector').strip()
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if comment:
            Review.objects.create(
                product=product,
                user=request.user if request.user.is_authenticated else None,
                name=name or (request.user.username if request.user.is_authenticated else 'Artisan Collector'),
                rating=rating,
                title=title or 'Exquisite Piece',
                comment=comment,
                is_approved=True
            )
            messages.success(request, "Thank you! Your ceramic review has been shared.")
        else:
            messages.error(request, "Please provide a review comment.")
    return redirect('products:product_detail', slug=product.slug)


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        wished = False
        msg = f"Removed {product.name} from your collection wishlist."
    else:
        wished = True
        msg = f"Added {product.name} to your collection wishlist."
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'wished': wished, 'message': msg})
    messages.info(request, msg)
    return redirect('products:product_detail', slug=product.slug)
