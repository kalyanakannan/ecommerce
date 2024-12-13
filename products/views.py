from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Product
from .serializer import ProductSerializer
from rest_framework.pagination import PageNumberPagination
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListCreateView(APIView):

    def get(self, request):
        try:
            products = Product.objects.all()
            paginator = ProductPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(paginated_products, many=True)
            logger.info("Successfully retrieved product list")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving products: {str(e)}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while fetching products."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            # Deserialize and validate input data
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Validation failed: {serializer.errors}")
                return Response(
                    {"error": "Invalid data provided.", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Custom validation for business logic (e.g., stock)
            stock = request.data.get("stock", None)
            if stock is not None and stock < 0:
                logger.warning(f"Invalid stock value: {stock}")
                return Response(
                    {"error": "Stock cannot be negative."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Save the product if everything is valid
            serializer.save()
            logger.info(f"Product created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}", exc_info=True)
            return Response(
                {"error": "A database integrity error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}", exc_info=True)
            return Response(
                {"error": "A validation error occurred.", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while creating the product."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
