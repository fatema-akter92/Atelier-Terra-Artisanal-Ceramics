from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product, Category, Review
from .models import NewsletterSubscriber, ContactInquiry


def home(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:6]
    bestsellers = Product.objects.filter(is_available=True, is_bestseller=True)[:4]
    categories = Category.objects.all()[:6]
    recent_reviews = Review.objects.filter(is_approved=True, rating__gte=4)[:4]

    # Special hero product: The Pleated Solstice Lamp (matches user photo)
    hero_lamp = Product.objects.filter(slug='pleated-solstice-table-lamp').first()

    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
        'recent_reviews': recent_reviews,
        'hero_lamp': hero_lamp,
    }
    return render(request, 'core/home.html', context)


def artisan_story(request):
    return render(request, 'core/artisan_story.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                subject=subject or 'Ceramic Atelier Inquiry',
                message=message
            )
            messages.success(request, "Your note has reached our workshop. We will reply within 24 hours.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'core/contact.html')


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    if email:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            msg = "Welcome to our ceramic community! Enjoy 10% off with code WARMTH10."
        else:
            msg = "You are already a cherished member of our atelier community."
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': msg})
        messages.success(request, msg)
    return redirect('core:home')
