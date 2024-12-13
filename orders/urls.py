from django.urls import path
from .views import OrderCreateView, OrderDetailsView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),
    path("<str:order_id>/", OrderDetailsView.as_view(), name="order-details")
]