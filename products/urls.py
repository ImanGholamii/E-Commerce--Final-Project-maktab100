from django.urls import path
from products.views import ProductDetailView
urlpatterns = [
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]