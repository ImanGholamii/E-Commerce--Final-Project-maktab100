import random
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils import send_otp_code
from users.forms import CustomUserCreationForm, VerifyCodeForm, EmployeeCreationForm, UserProfileForm, AddressForm
from users.models import UserProfile, OtpCode, Employee, Address
from users.serializers import UserProfileSerializer

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
            if 'guest_user' in request.COOKIES:
                print("Guest Cookie Data:", request.COOKIES)
                print("Guest Cookie Data:", request.COOKIES['guest_user'])
                guest_user_id = request.COOKIES['guest_user']
                # user = User.objects.get(id=guest_user_id)
                user = User.objects.get(id=int(guest_user_id))
                response = redirect('index')
                response.delete_cookie('guest_user')
                return response
            cart_data = request.session.get('cart', [])
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


# Profile

@login_required
def profile_view(request):
    view = UserProfileDetailView.as_view()
    response = view(request)
    user_profile_data = response.data

    view2 = UserDetailView.as_view()
    response2 = view2(request)
    user_data = response2.data

    view3 = AddressDetailView.as_view()
    response3 = view3(request)
    user_address = response3.data

    # user_profile = UserProfile.objects.get(user=request.user)
    # address = Address.objects.filter(user=request.user)

    # if request.method == 'POST' and request.FILES.get('profile_picture'):
    #     user_profile.profile_picture = request.FILES['profile_picture']
    #     user_profile.save()
    context = {'user_profile': user_profile_data,
               'user_data': user_data,
               'user_address': user_address,
               }
    print(user_profile_data)
    first_key, first_value = next(iter(user_profile_data.items()))
    print("First Key:", first_key, "First Value:", first_value)
    print('USER:USER:USER:USER:USER:USER:USER:', user_data)
    first_key, first_value = next(iter(user_data.items()))
    print("First Key:", first_key, "First Value:", first_value)
    # address
    print('ADDRESS:ADDRESS###########ADDRESS:ADDRESS:', user_address)
    for address in user_address:
        for key, value in address.items():
            print(f"{key}: {value}")
        print("\n")

    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            form.save()

            # Create AddressForm and assign request.user to the user field
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address_instance = address_form.save(commit=False)
                address_instance.user = request.user
                address_instance.save()

            return redirect('profile')

    else:
        address_form = AddressForm(initial={'user': request.user})

    user_addresses = Address.objects.filter(user_profiles=user_profile)
    context = {'form': form, 'user_addresses': user_addresses, 'address_form': address_form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def delete_address_view(request, pk):
    address = Address.objects.get(id=pk)

    if address.user == request.user:
        address.delete()

    return redirect('profile')


def home(request):
    return HttpResponse(f"Ola {request.user.username.upper()} ! 😊")


# Reset Password

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset/password_reset_done.html"
    title = _("Password reset link sent to your Email")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


# ============ API ============

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer, AddressSerializer


class UserProfileDetailView(APIView):
    def get(self, request, format=None):
        user_profile_data = self.request.user.userprofile
        serializer = UserProfileSerializer(user_profile_data)
        return Response(serializer.data)

    def put(self, request, format=None):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, format=None):
        user_data = self.request.user
        serializer = UserSerializer(user_data)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = User.objects.get(user=request.user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = Address.objects.get(user=request.user)
        user.address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressDetailView(APIView):
    def get(self, request, format=None):
        user_address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(user_address, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        user_address = Address.objects.get(user=request.user)
        serializer = AddressSerializer(user_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_address = Address.objects.get(id=pk)
        user_address.delete()
        return Response(status=status.HTTP_204_NO_CONTAddress)
