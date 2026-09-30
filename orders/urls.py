from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmed/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('track/', views.track_order, name='track_order'),
]
