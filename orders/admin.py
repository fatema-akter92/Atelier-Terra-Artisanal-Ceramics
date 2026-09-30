from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_name', 'item_type', 'price', 'quantity', 'custom_details']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'total_price', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'shipping_method', 'created_at']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'subtotal', 'discount_amount', 'shipping_cost', 'total_price', 'created_at', 'updated_at']
