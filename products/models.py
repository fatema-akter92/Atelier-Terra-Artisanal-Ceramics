from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fa-solid fa-shapes", help_text="FontAwesome icon class")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    story = models.TextField(blank=True, help_text="Artisan story, inspiration, clay origin")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=15)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_nook_hero = models.BooleanField(default=False, help_text="Available in the Cozy Nook Room Visualizer")
    
    # Visuals
    image = models.ImageField(upload_to="products/")
    
    # Artisanal Specifications
    material = models.CharField(max_length=200, default="Stoneware Clay & Natural Satin Glaze")
    dimensions = models.CharField(max_length=150, default="12\"H x 8\"W x 8\"D")
    weight = models.CharField(max_length=100, default="1.1 kg")
    firing_temperature = models.CharField(max_length=150, default="Cone 10 (1280°C / 2336°F)")
    care_instructions = models.TextField(default="Wipe with a soft damp cloth. Ceramic parts are water-resistant. Protect pleated shade from direct moisture.")
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. Handcrafted, Bestseller, Staff Pick")

    # Cozy Nook Room Builder Coordinates & Props
    nook_layer_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('lamp', 'Lamp on Desk'),
            ('vase', 'Vase on Desk'),
            ('cup', 'Pencil Cup on Desk'),
            ('wallmate', 'Wallmate on Brick Wall'),
            ('bowl', 'Bowl / Dish on Desk')
        ],
        help_text="Layer slot in Room Styler"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.slug])

    @property
    def discount_percent(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            return int(round((1 - (self.price / self.compare_at_price)) * 100))
        return 0

    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 5.0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.product.name} Gallery Image"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    title = models.CharField(max_length=150)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    verified_purchase = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}★ by {self.name} on {self.product.name}"
