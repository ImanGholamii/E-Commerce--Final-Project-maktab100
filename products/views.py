from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        context['product_images'] = product.images.all()
        context['category_path'] = product.category.get().get_full_path()
        return context
