from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'shipping_method', 'customer_notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street address, apartment or suite'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apartment, suite, unit (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Postal code'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'value': 'United States'}),
            'shipping_method': forms.Select(attrs={'class': 'form-select'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Special artisan packing instructions or gift message...'}),
        }
