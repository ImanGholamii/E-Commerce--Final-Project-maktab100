from django.urls import path
from users.views import SignUpView, login_view, profile_view, Logout, home, UserRegisterCodeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('verify/', UserRegisterCodeView.as_view(), name="verify"),
    # path('verify/resend_code/', UserRegisterCodeView.as_view(resend=True), name="resend_code"),
    path('login/', login_view, name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('users/profile/', profile_view, name="profile"),
    path('home/', home , name="home"),
]

