from django.urls import path

from core.drf_views import CoinAPIView, InventoryDetailAPIView, InventoryListAPIView

app_name = 'api'
urlpatterns = [
    path('', CoinAPIView.as_view()),
    path('inventory/', InventoryListAPIView.as_view()),
    path('inventory/<int:pk>/', InventoryDetailAPIView.as_view()),
]
