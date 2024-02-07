from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView, ListView

from orders.models import Order
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


# class ProductDetailView(LoginRequiredMixin, DetailView):
#     """to show product details probably in details page"""
#     model = Product
#     template_name = 'products/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         product = self.get_object()
#         context['all_categories'] = Category.objects.all()
#         context['product_images'] = product.images.all()
#         context['category_path'] = product.category.get().get_full_path()
#         context['category_root'] = product.category.get().get_root_categories_queryset()
#         context['category'] = product.category.get()
#         return context


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


def homeview(request):
    template_name = 'index.html'
    paginate_by = 6

    product_list = Product.objects.all()
    category = request.GET.get('category')

    if category:
        product_list = product_list.filter(category__name=category)

    paginator = Paginator(product_list, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user.username if request.user.is_authenticated else 'AnonymousUser'
    form = CustomUserCreationForm()

    customer = None
    order = None
    cartItems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_items.select_related('order')
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {
        'product_list': page_obj,
        'user': user,
        'form': form,
        'all_categories': Category.objects.all(),
        'customer': customer,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, template_name, context)

@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.order_items.all()
        cart_items = order.get_cart_items
    else:
        order = None
        order_items = []
        cart_items = 0

    context = {
        'order': order,
        'order_items': order_items,
        'cart_items': cart_items,
    }
    return render(request, 'products/cart.html', context)


@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.order_items.all()
        cart_items = order_items.count()
    else:
        order = None
        order_items = []
        cart_items = 0

    context = {
        'order': order,
        'order_items': order_items,
        'cart_items': cart_items,
    }
    return render(request, 'products/checkout.html', context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from imagess.models import ProductImages
from products.serializers import ProductSerializer
from imagess.serializers import ProductImagesSerializer


class ProductDetailApiView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product_serializer = ProductSerializer(product).data
            product_images = ProductImages.objects.filter(product=product)
            product_images_serializer = ProductImagesSerializer(product_images, many=True).data
            return Response({'product': product_serializer, 'images': product_images_serializer},
                            status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


from django.shortcuts import render
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        response = ProductDetailApiView.as_view()(self.request, pk=pk)
        if response.status_code == status.HTTP_200_OK:
            product_data = response.data
            context['product_data'] = product_data
        else:
            context['error_message'] = 'Product not found'
        return context

