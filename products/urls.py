from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('item/<int:product_id>/review/', views.submit_review, name='submit_review'),
    path('item/<int:product_id>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
]
