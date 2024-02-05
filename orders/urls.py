from django.urls import path
from .views import CreateShoppingCartView, ShoppingCartDetailView, AddProductToCartView, CancelOrderView

urlpatterns = [
    path('create-shopping-cart/', CreateShoppingCartView.as_view(), name='create-shopping-cart'),
    path('shopping-cart/', ShoppingCartDetailView.as_view(), name='shopping-cart'),
    path('add-product-to-cart/', AddProductToCartView.as_view(), name='add-product-to-cart'),
    path('cancel-order/<int:order_id>/', CancelOrderView.as_view(), name='cancel-order'),
]
