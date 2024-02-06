from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from products.models import Product, Category
from users.forms import CustomUserCreationForm


def template_render(request):
    """Temporary view just to show home page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(LoginRequiredMixin, DetailView):
    """to show product details probably in details page"""
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        context['all_categories'] = Category.objects.all()
        context['product_images'] = product.images.all()
        context['category_path'] = product.category.get().get_full_path()
        context['category_root'] = product.category.get().get_root_categories_queryset()
        context['category'] = product.category.get()
        return context


class ProductCategoryListView(ListView):
    template_name = "products/product_category.html"
    model = Product

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_categories'] = Category.objects.all()
        # context['all_categories'] = Category.objects.all().filter(parent__is_active=True)

        context['parent_categories'] = context['all_categories'].filter(parent=None)

        context['parent_category'] = Category.objects.get(name=self.kwargs['category_name'])
        return context


class ParentCategoryListView(ListView):
    template_name = "products/parent_category.html"
    model = Category
    context_object_name = 'child_categories'

    def get_queryset(self):
        parent_category_name = self.kwargs['category_name']
        parent_category = get_object_or_404(Category, name=parent_category_name)
        return Category.objects.filter(parent=parent_category, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_category'] = get_object_or_404(Category, name=self.kwargs['category_name'])
        context['all_categories'] = Category.objects.all()
        return context


class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'product_list'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category__name=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = CustomUserCreationForm()
        context['form'] = form
        context['all_categories'] = Category.objects.all()
        # context['all_categories'] = Category.objects.all().filter(parent__is_active=True)
        return context
