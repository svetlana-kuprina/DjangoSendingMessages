
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, email_verification_user, PasswordRecovery, \
    email_verification_user2, UserListView, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>", email_verification_user, name="activate"),
    path("password_recovery/", PasswordRecovery.as_view(), name="password_recovery"),
    path("password_recovery2/<str:token>/", email_verification_user2, name="password_recovery2"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
]