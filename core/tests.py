from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from atelier.models import CeramicShape, GlazeOption, CustomCreation
from orders.models import Order, OrderItem


class AtelierCeramicsTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Category
        self.category = Category.objects.create(
            name="Ambient Lighting",
            slug="ambient-lighting",
            description="Warm lamps and pleated shades",
            icon="fa-solid fa-lightbulb"
        )

        # Product matching user image
        self.lamp = Product.objects.create(
            category=self.category,
            name="The Pleated Solstice Table Lamp",
            slug="pleated-solstice-table-lamp",
            tagline="Hand-pleated paper shade on powder-coated architectural iron tripod",
            description="Signature hero lamp matching user photo.",
            price=Decimal("145.00"),
            compare_at_price=Decimal("180.00"),
            stock=10,
            is_available=True,
            is_featured=True,
            is_bestseller=True,
            is_nook_hero=True,
            nook_layer_type="lamp",
            image="products/pleated_solstice_lamp.jpg"
        )

        # Atelier Shape & Glaze
        self.shape = CeramicShape.objects.create(
            name="The Pleated Solstice Table Lamp",
            slug="custom-pleated-lamp",
            base_price=Decimal("145.00"),
            shape_code="pleated_lamp"
        )

        self.glaze = GlazeOption.objects.create(
            name="Speckled Oatmeal",
            hex_color="#F2EDE4",
            accent_color="#DFD5C6",
            texture_type="speckled",
            price_modifier=Decimal("0.00")
        )

        # User
        self.user = User.objects.create_user(
            username="testcollector",
            email="test@atelier.com",
            password="securepassword123"
        )

    def test_home_page_status_and_content(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ATELIER TERRA")
        self.assertContains(response, "The Pleated Solstice Table Lamp")
        self.assertContains(response, "Custom Studio")

    def test_product_list_and_category_filter(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Pleated Solstice Table Lamp")

        cat_response = self.client.get(reverse('products:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(cat_response.status_code, 200)
        self.assertContains(cat_response, "Ambient Lighting")

    def test_product_detail(self):
        response = self.client.get(reverse('products:product_detail', args=[self.lamp.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "$145.00")
        self.assertContains(response, "Cone 10")

    def test_cart_add_and_coupon(self):
        # Add lamp to cart
        response = self.client.post(reverse('cart:cart_add', args=[self.lamp.id]), {'quantity': 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Added &#x27;The Pleated Solstice Table Lamp&#x27; to your cart.")

        # Apply coupon WARMTH10
        coupon_res = self.client.post(reverse('cart:apply_coupon'), {'code': 'WARMTH10'}, follow=True)
        self.assertEqual(coupon_res.status_code, 200)
        self.assertContains(coupon_res, "10% Warmth Discount Applied!")

    def test_custom_atelier_creation(self):
        # Studio page
        studio_res = self.client.get(reverse('atelier:studio'))
        self.assertEqual(studio_res.status_code, 200)

        # Submit custom creation
        custom_post = self.client.post(reverse('atelier:create_custom_ceramic'), {
            'shape_id': self.shape.id,
            'glaze_id': self.glaze.id,
            'finish_texture': 'speckled',
            'lamp_stand_color': 'brass',
            'engraving_text': 'A.T. 2026',
        }, follow=True)

        self.assertEqual(custom_post.status_code, 200)
        self.assertTrue(CustomCreation.objects.filter(engraving_text='A.T. 2026').exists())
        self.assertContains(custom_post, "Custom The Pleated Solstice Table Lamp")

    def test_cozy_nook_bundle_add(self):
        nook_res = self.client.get(reverse('atelier:cozy_nook_builder'))
        self.assertEqual(nook_res.status_code, 200)
        self.assertContains(nook_res, "Style My Morning Desk Nook")

        bundle_res = self.client.post(reverse('atelier:add_nook_bundle'), {
            'product_ids': f'[{self.lamp.id}]'
        }, follow=True)
        self.assertEqual(bundle_res.status_code, 200)
        self.assertContains(bundle_res, "15% bundle discount")

    def test_checkout_and_order_flow(self):
        # Add item to cart
        self.client.post(reverse('cart:cart_add', args=[self.lamp.id]), {'quantity': 1})

        # Checkout
        checkout_res = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Maya',
            'last_name': 'Kovac',
            'email': 'maya@example.com',
            'phone': '555-0192',
            'address_line1': '123 Pine St',
            'city': 'Seattle',
            'state': 'WA',
            'postal_code': '98101',
            'country': 'United States',
            'shipping_method': 'standard',
            'customer_notes': 'Please pack with extra pine wrap',
        }, follow=True)

        self.assertEqual(checkout_res.status_code, 200)
        self.assertTrue(Order.objects.filter(email='maya@example.com').exists())
        order = Order.objects.get(email='maya@example.com')
        self.assertContains(checkout_res, order.order_number)

        # Check stock decrement
        self.lamp.refresh_from_db()
        self.assertEqual(self.lamp.stock, 9)

        # Track order
        track_res = self.client.get(reverse('orders:track_order') + f'?order_number={order.order_number}&email={order.email}')
        self.assertEqual(track_res.status_code, 200)
        self.assertContains(track_res, order.order_number)
