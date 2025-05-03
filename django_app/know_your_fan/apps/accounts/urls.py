from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from apps.accounts.views.create_user_info_view import CreateUserInfoView
from apps.accounts.views.create_custom_user_view import CreateCustomUserView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('register/', CreateCustomUserView.as_view(), name='register'),
    path('validation/', CreateUserInfoView.as_view(), name='validation'),
]
