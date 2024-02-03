from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from core.utils import send_otp_code
from users.forms import CustomUserCreationForm, VerifyCodeForm, EmployeeCreationForm
from users.models import UserProfile, OtpCode, Employee
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()


def generate_otp_code():
    return random.randint(100000, 999999)


class SignUpView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('verify')
    login_url = '/users/login/'

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            random_code = generate_otp_code()
            send_otp_code(
                recipient=form.cleaned_data['email'],
                subject='FAST FOODIA Verification Code',
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
            return HttpResponseRedirect(self.success_url)

        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        group_name = _('Customer')
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        user.save()
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


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
                user_instance.is_customer = True
                user_instance.is_employee = False
                group_name = _('Customer')
                employee_group, created = Group.objects.get_or_create(name=group_name)
                user_instance.groups.add(employee_group)
                user_instance.save()
                code_instance.delete()
                messages.success(request, "Your account Verified successfully", 'success')
                return redirect('login')
            else:
                messages.error(request, 'Wrong Code!', 'danger')
                return redirect('verify')
        return redirect('/')


class EmployeeSignUpView(CreateView):
    model = get_user_model()
    form_class = EmployeeCreationForm
    template_name = 'users/employee_sign_up.html'
    success_url = reverse_lazy('verify_employee')
    login_url = '/users/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            random_code = generate_otp_code()
            send_otp_code(
                recipient=form.cleaned_data['email'],
                subject='FAST FOODIA Verification Code',
                message=f'Your verification code is: {random_code}',
            )
            OtpCode.objects.create(email=form.cleaned_data['email'], otp_code=random_code)
            request.session['user_registration_info'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'password': form.cleaned_data['password1'],
                'employee_role': form.cleaned_data['role'],
            }
            messages.success(request, 'OTP Code Sent to your email.', 'success')
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        group_name = _('Employee')
        employee_group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(employee_group)
        user.save()
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class EmployeeRegisterCodeView(View):
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
                user_instance.is_customer = False
                user_instance.is_employee = True
                user_instance.is_staff = True
                group_name = _('Employee')
                employee_group, created = Group.objects.get_or_create(name=group_name)
                user_instance.groups.add(employee_group)
                user_instance.save()
                employee_instance = Employee.objects.create(
                    user=user_instance,
                    role=user_session['employee_role'],
                    is_manager=user_session['employee_role'] == 'manager',
                    is_operator=user_session['employee_role'] == 'operator',
                    is_viewer=user_session['employee_role'] == 'viewer',
                )
                employee_instance.save()
                code_instance.delete()
                messages.success(request, "Your account Verified successfully", 'success')
                return redirect('login')
            else:
                messages.error(request, 'Wrong Code!', 'danger')
                return redirect('verify')
        return redirect('/')


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


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()

    context = {'user_profile': user_profile}
    return render(request, 'users/profile.html', context)


def home(request):
    return HttpResponse(f"Ola {request.user.username.upper()} ! 😊")


# Password Reset Views

# def send_password_reset_email(request, user_id):
#     """Generate a token for the user"""
#     user = get_object_or_404(User, pk=user_id)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#
#     reset_url = f"{settings.BASE_URL}/users/reset_password/{uid}/{token}/"
#
#     subject = 'Password Reset Request'
#     message = render_to_string('users/password_reset.html', {
#         'user': user,
#         'reset_url': reset_url,
#     })
#
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
#
#
# def reset_password(uidb64, token, new_password):
#     """ Decode the uid and get the user """
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = get_user_model().objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#         user = None
#
#     if user is not None and default_token_generator.check_token(user, token):
#
#         user.set_password(new_password)
#         user.save()
#         return True
#     else:
#         return False
#
#
# class PasswordResetView(View):
#     def get(self, request, uidb64, token):
#         return render(request, 'users/password_reset.html', {'uidb64': uidb64, 'token': token})
#
#     def post(self, request, uidb64, token):
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#
#         if new_password == confirm_password:
#             try:
#                 uid = force_str(urlsafe_base64_decode(uidb64))
#                 user = get_user_model().objects.get(pk=uid)
#             except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#                 user = None
#
#             if user is not None and default_token_generator.check_token(user, token):
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, 'Password has been reset successfully.')
#                 return redirect('login')
#             else:
#                 messages.error(request, 'Invalid link for password reset.')
#         else:
#             messages.error(request, 'Passwords do not match.')
#
#         return render(request, 'users/password_reset.html', {'uidb64': uidb64, 'token': token})

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset/password_reset_done.html"
    title = _("Password reset sent")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context
