from django.urls import path
from . import views

app_name = 'atelier'

urlpatterns = [
    path('studio/', views.atelier_studio, name='studio'),
    path('studio/create/', views.create_custom_ceramic, name='create_custom_ceramic'),
    path('cozy-nook/', views.cozy_nook_builder, name='cozy_nook_builder'),
    path('cozy-nook/add-bundle/', views.add_nook_bundle_to_cart, name='add_nook_bundle'),
]
