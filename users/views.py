from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from users.forms import CustomUserCreationForm
from users.models import UserProfile
from django.utils.translation import gettext_lazy as _


class SignUpView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    # template_name = 'users/sign_up.html'
    template_name = 'index.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        customer = form.cleaned_data['is_customer']
        if customer == True:
            group = Group.objects.get(name=_('Customer'))
        if not customer:
            group = Group.objects.get(name=_('Employee'))

        user.save()
        user.groups.add(group)
        return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.session.get('next')
            if next_url:
                del request.session['next']
                return redirect(next_url)
            return redirect('/')
        else:
            return render(request, 'users/login.html')

    next_url = request.GET.get('next')
    if next_url:
        request.session['next'] = next_url

    return render(request, 'users/login.html')


class Logout(View):
    def get(self, request):
        if self.request.user:
            latest_user_login = request.user.username
            logout(request)
            response = redirect('home')
            response.set_cookie('latest_user_login', latest_user_login)
            return response


def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_addresses = user_profile.addresses.all()
    context = {'user_profile': user_profile, 'user_addresses': user_addresses}
    return render(request, 'users/profile.html', context)


def home(request):
    return HttpResponse(f"Ola {request.user.username.upper()} ! 😊")
