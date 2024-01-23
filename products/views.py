from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from products.models import Product
from users.forms import CustomUserCreationForm



def template_render(request):
    """Temporary view just to show home page"""
    return render(request, 'index.html')

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = CustomUserCreationForm()
        context['form'] = form

        return context

class ProductListView(ListView):
    model = Product
    template_name = 'index.html'

class ProductDetailView(DetailView):
    """to show product details probably in details page"""
    model = Product
    template_name = 'products/templates/products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        context['product_images'] = product.images.all()
        context['category_path'] = product.category.get().get_full_path()
        return context
