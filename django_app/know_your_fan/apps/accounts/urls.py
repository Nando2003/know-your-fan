from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from apps.accounts.views.wait_validation_view import WaitingValidationView
from apps.accounts.views.create_custom_user_view import CreateCustomUserView
from apps.accounts.views.create_request_user_info_view import CreateRequestUserInfoView
from apps.accounts.views.check_validation_status_view import check_validation_status_view
from apps.accounts.views.create_user_info_webhook_view import validation_webhook_view

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('register/', CreateCustomUserView.as_view(), name='register'),
    path('validation/', CreateRequestUserInfoView.as_view(), name='validation'),
    path('validation/waiting/', WaitingValidationView.as_view(), name='waiting_validation'),
    path('validation/check/', check_validation_status_view, name='check_validation_status'),
    path('webhook/', validation_webhook_view, name='webhook'),

]
