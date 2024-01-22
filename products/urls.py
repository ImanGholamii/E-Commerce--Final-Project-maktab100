from django.urls import path
from products.views import ProductDetailView, template_render, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
