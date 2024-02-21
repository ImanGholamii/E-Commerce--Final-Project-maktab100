from django.urls import path
from .views import OrderApiVew, OrderUpdateDeleteView, OrderItemApiView, OrderListCreateView, \
    OrderItemUpdateDeleteApiView, check_cart, submit_order

urlpatterns = [
    path('', OrderApiVew.as_view(), name='add-to-cart'),
    path('<int:pk>/', OrderUpdateDeleteView.as_view()),
    path('items/', OrderItemApiView.as_view()),
    path('items/<int:pk>', OrderItemUpdateDeleteApiView.as_view()),
    path('cart/', check_cart, name="cart"),
    path('submitted/', submit_order, name="submit_order"),

]
