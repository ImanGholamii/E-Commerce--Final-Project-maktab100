from django.urls import path
from users.views import SignUpView, login_view, profile_view, Logout, home, UserRegisterCodeView, EmployeeSignUpView, \
    EmployeeRegisterCodeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, edit_profile_view, delete_address_view, UserProfileDetailView, AddressDetailView, AddressUpdateDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('signup/employee/', EmployeeSignUpView.as_view(), name="employee_signup"),
    path('verify/', UserRegisterCodeView.as_view(), name="verify"),
    path('verify/employee/', EmployeeRegisterCodeView.as_view(), name="verify_employee"),
    # path('verify/resend_code/', UserRegisterCodeView.as_view(resend=True), name="resend_code"),
    path('login/', login_view, name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('profile/', profile_view, name="profile"),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('delete-address/<int:pk>/', delete_address_view, name='delete_address'),
    path('home/', home, name="home"),
    # Reset Password
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # API
    path('api/profile/', UserProfileDetailView.as_view(), name='api_profile'),
    path('api/address/', AddressDetailView.as_view(), name='api_profile'),
    path('api/address/update/<int:pk>/', AddressUpdateDeleteView.as_view(), name='address_update_api'),
]
