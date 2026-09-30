from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class CeramicShape(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    category_label = models.CharField(max_length=80, default="Ceramic Vessel")
    description = models.TextField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    dimensions = models.CharField(max_length=100, default="10\"H x 7\"W")
    shape_code = models.CharField(
        max_length=50,
        help_text="Key used by the interactive canvas renderer: pleated_lamp, fluted_vase, donut_flask, desk_cup, tea_bowl"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} (${self.base_price})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GlazeOption(models.Model):
    name = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=20, help_text="e.g. #F2EDE4")
    accent_color = models.CharField(max_length=20, default="#DFD5C6", help_text="Secondary gradient / shade tone")
    texture_type = models.CharField(
        max_length=50,
        choices=[
            ('speckled', 'Speckled Mineral Sand'),
            ('satin_matte', 'Smooth Satin Matte'),
            ('ribbed_tactile', 'Tactile Ribbed Flute'),
            ('terracotta_raw', 'Raw Fired Terracotta'),
            ('crackle_celadon', 'Crackle Glaze Celadon')
        ],
        default='speckled'
    )
    description = models.CharField(max_length=255, blank=True)
    price_modifier = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. Signature Glaze, Most Loved")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_texture_type_display()})"


class CustomCreation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=60, blank=True)
    shape = models.ForeignKey(CeramicShape, on_delete=models.CASCADE)
    glaze = models.ForeignKey(GlazeOption, on_delete=models.CASCADE)
    finish_texture = models.CharField(max_length=50, default="speckled")
    lamp_stand_color = models.CharField(
        max_length=50,
        choices=[
            ('white', 'Alabaster Architectural Iron'),
            ('brass', 'Warm Brushed Brass'),
            ('matte_black', 'Forged Matte Black')
        ],
        default='white'
    )
    engraving_text = models.CharField(max_length=30, blank=True, help_text="Artisan stamp under base (e.g. initials or year)")
    preview_data_url = models.TextField(blank=True, help_text="Base64 or canvas snapshot")
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom {self.shape.name} in {self.glaze.name} (${self.final_price})"
