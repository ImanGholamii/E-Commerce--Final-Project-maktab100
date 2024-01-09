from django.urls import path
from users.views import SignUpView, login_view, profile_view, Logout, home

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('users/profile/', profile_view , name="profile"),
    path('home/', home , name="home"),
]

