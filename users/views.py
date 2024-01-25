from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from core.utils import send_otp_code
from users.forms import CustomUserCreationForm, VerifyCodeForm
from users.models import UserProfile, OtpCode
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
import random


class SignUpView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/sign_up.html'
    # template_name = 'index.html'
    # success_url = reverse_lazy('login')
    success_url = reverse_lazy('verify')

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            random_code = random.randint(100000, 999999)
            send_otp_code(
                recipient=form.cleaned_data['email'],
                subject='Verification Code',
                message=f'Your verification code is: {random_code}',
            )
            OtpCode.objects.create(email=form.cleaned_data['email'], otp_code=random_code)
            request.session['user_registration_info'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'password': form.cleaned_data['password1'],
            }
            messages.success(request, 'OTP Code Sent to your email.', 'success')
        return HttpResponseRedirect(reverse_lazy('verify'))

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

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserRegisterCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        user_session = request.session['user_registration_info']
        print(44 * '=' + 'user_session' + 44 * '=')
        print(user_session)
        form = self.form_class
        return render(request, 'users/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(email=user_session['email'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.otp_code:
                User = get_user_model()
                user_instance = User.objects.create_user(user_session['email'], user_session['phone'],
                                                         user_session['password'])
                user_instance.username = user_session['username']
                user_instance.save()
                code_instance.delete()
                messages.success(request, "Your account Verified successfully", 'success')
                return redirect('login')
            else:
                messages.error(request, 'Wrong Code!', 'danger')
                return redirect('verify')
        return redirect('/')


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             next_url = request.session.get('next')
#             if next_url:
#                 del request.session['next']
#                 return JsonResponse({'success': True, 'next_url': next_url})
#             return JsonResponse({'success': True, 'next_url': '/'})
#         else:
#             return JsonResponse({'success': False, 'next_url': 'users/login.html'})
#
#     next_url = request.GET.get('next')
#     if next_url:
#         request.session['next'] = next_url
#
#     return render(request, 'users/login.html')

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
            response = redirect('/')
            response.set_cookie('latest_user_login', latest_user_login)
            return response


def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_addresses = user_profile.addresses.all()
    context = {'user_profile': user_profile, 'user_addresses': user_addresses}
    return render(request, 'users/profile.html', context)


def home(request):
    return HttpResponse(f"Ola {request.user.username.upper()} ! 😊")
