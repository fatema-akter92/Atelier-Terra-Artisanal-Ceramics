from django.contrib import admin
from django.utils.html import format_html
from .models import CeramicShape, GlazeOption, CustomCreation


@admin.register(CeramicShape)
class CeramicShapeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_label', 'base_price', 'shape_code', 'is_active', 'order']
    list_editable = ['base_price', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GlazeOption)
class GlazeOptionAdmin(admin.ModelAdmin):
    list_display = ['color_swatch', 'name', 'texture_type', 'price_modifier', 'badge', 'is_active']
    list_editable = ['price_modifier', 'is_active']

    def color_swatch(self, obj):
        return format_html(
            '<div style="display:flex; align-items:center; gap:8px;">'
            '<span style="width:24px; height:24px; border-radius:50%; background-color:{}; border:1px solid #ccc; display:inline-block;"></span>'
            '<span>{}</span>'
            '</div>',
            obj.hex_color, obj.name
        )
    color_swatch.short_description = 'Glaze Swatch'


@admin.register(CustomCreation)
class CustomCreationAdmin(admin.ModelAdmin):
    list_display = ['id', 'shape', 'glaze', 'finish_texture', 'engraving_text', 'final_price', 'created_at']
    list_filter = ['shape', 'glaze', 'finish_texture', 'created_at']
    search_fields = ['engraving_text', 'user__username', 'session_key']
