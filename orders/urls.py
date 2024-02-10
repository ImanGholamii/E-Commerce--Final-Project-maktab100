from django.urls import path
from .views import OrderApiVew, OrderUpdateDeleteView, OrderListCreateView

urlpatterns = [
    path('', OrderApiVew.as_view()),
    path('<int:pk>/', OrderUpdateDeleteView.as_view()),
    # path('', OrderListCreateView.as_view()),
]
