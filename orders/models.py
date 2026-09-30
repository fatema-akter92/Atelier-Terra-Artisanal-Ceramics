import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Order Received'),
        ('confirmed', 'Artisan Confirmed'),
        ('in_kiln', 'Glazing & Kiln Firing'),
        ('inspected', 'Artisan Quality Inspected'),
        ('shipped', 'Carefully Dispatched'),
        ('delivered', 'Delivered to Home'),
    ]

    SHIPPING_CHOICES = [
        ('standard', 'Eco-Conscious Standard Delivery ($12.00 or Free over $150)'),
        ('fragile_white_glove', 'Fragile Ceramic White-Glove Courier ($25.00)'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="United States")

    shipping_method = models.CharField(max_length=30, choices=SHIPPING_CHOICES, default='standard')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='confirmed')
    payment_status = models.CharField(max_length=20, default='paid')
    customer_notes = models.TextField(blank=True, help_text="Gift message or special handling note")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"AT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    item_type = models.CharField(max_length=20, default='product')
    item_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    custom_details = models.TextField(blank=True, help_text="Glaze, texture, stamp text if custom piece")
    preview_data_url = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.item_name} on Order #{self.order.order_number}"

    @property
    def total_cost(self):
        return self.price * self.quantity
