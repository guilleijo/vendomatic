from django.urls import path

from core.drf_views import CoinAPIView, InventoryDetailAPIView, InventoryListAPIView

app_name = 'api'
urlpatterns = [
    path('', CoinAPIView.as_view(), name='coin'),
    path('inventory/', InventoryListAPIView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/', InventoryDetailAPIView.as_view(), name='inventory-detail'),
]
