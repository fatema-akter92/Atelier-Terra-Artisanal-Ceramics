from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'price', 'compare_at_price', 'stock', 'is_available', 'is_featured', 'is_bestseller']
    list_filter = ['category', 'is_available', 'is_featured', 'is_bestseller', 'nook_layer_type']
    list_editable = ['price', 'stock', 'is_available', 'is_featured', 'is_bestseller']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'material']
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Thumbnail'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'title', 'comment', 'product__name']
