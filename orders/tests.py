from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, OrderItem
from products.models import Product
from .serializer import OrderItemSerializer, OrderSerializer
import uuid

class OrderTestCase(TestCase):
    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(name="Sample Product", stock=10, price=100.0)

    def test_order_model_str(self):
        order = Order.objects.create(status="pending", total_price=200.0)
        self.assertEqual(str(order), f"Order {order.id}")

    def test_order_item_model_str(self):
        order = Order.objects.create(status="pending", total_price=200.0)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        self.assertEqual(str(order_item), f"Item {self.product.name} in Order {order.id}")

class OrderSerializerTestCase(TestCase):
    def setUp(self):
        # Create a sample product
        self.product = Product.objects.create(name="Sample Product", stock=10, price=100.0)

    def test_validate_products_empty(self):
        data = {
            "status": "pending",
            "total_price": 0.0,
            "products": []
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("products", serializer.errors)

    def test_validate_insufficient_stock(self):
        data = {
            "status": "pending",
            "total_price": 200.0,
            "products": [
                {"product": self.product.id, "quantity": 20}
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("products", serializer.errors)

    def test_create_order_successful(self):
        data = {
            "status": "pending",
            "total_price": 200.0,
            "products": [
                {"product": self.product.id, "quantity": 2}
            ]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.total_price, 200.0)

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name="Sample Product", stock=10, price=100.0)
        self.order = Order.objects.create(status="pending", total_price=200.0)

    def test_order_create_view_success(self):
        data = {
            "status": "pending",
            "total_price": 200.0,
            "products": [
                {"product": self.product.id, "quantity": 2}
            ]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_create_view_failure(self):
        data = {
            "status": "pending",
            "total_price": 200.0,
            "products": [
                {"product": self.product.id, "quantity": 20}
            ]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_details_view_success(self):
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_details_view_not_found(self):
        invalid_id = 1000
        response = self.client.get(f'/api/orders/{invalid_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
