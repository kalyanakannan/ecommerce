from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from .serializer import OrderSerializer
import logging
from django.http import Http404

logger = logging.getLogger(__name__)


class OrderCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(f"Validation failed: {serializer.errors}")
            return Response(
                {"error": "Invalid data provided.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = serializer.save()
            logger.info(f"Order {order.id} created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Unexpected error while creating order: {str(e)}", exc_info=True)
            return Response(
                {"error": "An unexpected error occurred while processing the order."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderDetailsView(APIView):
    def get(self, request, order_id):
        try:
            logger.info(f"Fetching order with ID: {order_id}")
            order = get_object_or_404(Order, id=order_id)
            serializer = OrderSerializer(order)
            logger.info(f"Order {order.id} retrieved successfully.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Http404:
            logger.warning(f"Order with ID {order_id} not found.")
            return Response(
                {"error": f"Order with ID {order_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Order.DoesNotExist:
            logger.warning(f"Order with ID {order_id} does not exist.")
            return Response(
                {"error": f"Order with ID {order_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error retrieving order {order_id}: {str(e)}", exc_info=True)
            return Response(
                {"error": f"An unexpected error occurred while retrieving order {order_id}."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

