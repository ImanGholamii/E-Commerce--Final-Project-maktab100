from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from products.models import Product
from users.forms import CustomUserCreationForm


def template_render(request):
    """Temporary view just to show home page"""
    return render(request, 'index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'


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


from django.contrib.auth.views import LoginView

class HomeView(LoginView, ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'product_list'
    form_class = AuthenticationForm  # اضافه کردن فرم ورود به سیستم

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category__name=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # اضافه کردن فرم ثبت‌نام به context
        registration_form = CustomUserCreationForm()
        context['registration_form'] = registration_form

        return context

    def post(self, request, *args, **kwargs):
        # گرفتن اطلاعات از فرم ورود به سیستم
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # اجرای اعتبارسنجی ورود به سیستم
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        # اجرای اعتبارسنجی ناموفق
        registration_form = CustomUserCreationForm()
        context = {'registration_form': registration_form, 'login_form': form}
        return self.render_to_response(self.get_context_data(**context))
