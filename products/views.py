from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
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

    def  get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """to show product details probably in details page"""
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        context['product_images'] = product.images.all()
        context['category_path'] = product.category.get().get_full_path()
        return context


class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'product_list'

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

        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("User Registered Successfully!")
            print("Username:", form.cleaned_data['username'])
            print("Email:", form.cleaned_data['email'])
            print("Phone:", form.cleaned_data['phone'])
            print("Is Customer:", form.cleaned_data['is_customer'])
        context = {'form': form}
        return render(request, self.template_name, context)


class ProductCategoryListView(ListView):
    template_name = "products/product_category.html"
    model = Product

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_categories'] = Category.objects.get_root_categories_queryset()
        context['parent_category'] = Category.objects.get(name=self.kwargs['category_name'])
        return context
# from django.contrib.auth.views import LoginView
#
# class HomeView(ListView, LoginView):
#     model = Product
#     template_name = 'index.html'
#     context_object_name = 'product_list'
#     form_class = AuthenticationForm  # اضافه کردن فرم ورود به سیستم
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category = self.request.GET.get('category')
#
#         if category:
#             queryset = queryset.filter(category__name=category)
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # اضافه کردن فرم ثبت‌نام به context
#         registration_form = CustomUserCreationForm()
#         context['registration_form'] = registration_form
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         # اجرای اعتبارسنجی ناموفق
#         registration_form = CustomUserCreationForm()
#         context = {'registration_form': registration_form, 'login_form': form}
#         return self.render_to_response(self.get_context_data(**context))
