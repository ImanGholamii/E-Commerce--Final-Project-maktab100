from django.urls import path
from products.views import ProductDetailView, template_render

urlpatterns = [
    path('', template_render, name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
