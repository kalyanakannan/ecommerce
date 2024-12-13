from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product


class ProductListCreateViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.valid_product = {
            "name": "Test Product",
            "description": "A test product description.",
            "price": 99.99,
            "stock": 10,
        }
        self.invalid_product_price = {
            "name": "Invalid Product",
            "description": "Invalid test product.",
            "price": -1,  # Negative price
            "stock": 5,
        }
        self.invalid_product_stock = {
            "name": "Invalid Stock Product",
            "description": "Invalid test product stock.",
            "price": 50,
            "stock": -5,  # Negative stock
        }
        # Create some initial products for GET testing
        Product.objects.create(name="Existing Product", description="Existing product desc.", price=25.0, stock=15)

    def test_get_products(self):
        """Test retrieving the list of products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)  # Only one existing product

    def test_create_valid_product(self):
        """Test creating a valid product"""
        response = self.client.post('/api/products/', self.valid_product, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.valid_product["name"])
        self.assertEqual(response.data["price"], self.valid_product["price"])
        self.assertEqual(response.data["stock"], self.valid_product["stock"])

    def test_create_product_with_negative_price(self):
        """Test creating a product with negative price"""
        response = self.client.post('/api/products/', self.invalid_product_price, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("price", response.data["details"])

    def test_create_product_with_negative_stock(self):
        """Test creating a product with negative stock"""
        response = self.client.post('/api/products/', self.invalid_product_stock, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("stock", response.data["details"])
