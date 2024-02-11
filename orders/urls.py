from django.urls import path
from .views import OrderApiVew, OrderUpdateDeleteView, OrderItemApiView, OrderListCreateView, \
    OrderItemUpdateDeleteApiView

urlpatterns = [
    path('', OrderApiVew.as_view()),
    path('<int:pk>/', OrderUpdateDeleteView.as_view()),
    path('items/', OrderItemApiView.as_view()),
    path('items/<int:pk>', OrderItemUpdateDeleteApiView.as_view()),

]
