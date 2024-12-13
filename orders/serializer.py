from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True) 

    class Meta:
        model = Order
        fields = "__all__"

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError("Order items cannot be empty.")
        for item in value:
            product = Product.objects.get(id=item.get("product").id)
            quantity = item.get('quantity')
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for product '{product.name}'. Available: {product.stock}, Requested: {quantity}."
                )
            if quantity <= 0:
                raise serializers.ValidationError(f"Quantity must be greater than zero for product '{product.name}'.")
        return value

    def validate(self, data):
        if data.get("total_price", 0) <= 0:
            raise serializers.ValidationError("Total price must be greater than zero.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        products_data = self.initial_data.get('products', [])
        order = Order.objects.create(
            status=validated_data['status'],
            total_price=validated_data['total_price']
        )

        for item_data in products_data:
            product = Product.objects.get(id=item_data['product'])
            quantity = item_data['quantity']
            product.stock -= quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item_data['price']
            )

        return order
    
    def to_representation(self, instance):
        """Customize the response to rename `order_items` to `products`."""
        representation = super().to_representation(instance)
        representation['products'] = representation.pop('order_items')  # Rename key in the response
        return representation
