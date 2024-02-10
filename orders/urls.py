from django.urls import path
from .views import OrderApiVew, OrderListCreateView

urlpatterns = [
    path('', OrderApiVew.as_view()),
    # path('', OrderListCreateView.as_view()),
]
