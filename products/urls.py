from django.urls import path
from products.views import ProductDetailView, HomeView, ProductListView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
