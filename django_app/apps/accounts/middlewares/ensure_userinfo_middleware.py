from django.shortcuts import redirect
from django.urls import reverse
from apps.accounts.models import UserInfo

EXEMPT_PATHS = [
    'userinfo_create',  # nome da URL da view de criação do perfil
    'logout',
    'admin:login',
    'admin:index',
]

class EnsureUserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                request.user.userinfo
            except UserInfo.DoesNotExist:
                current_view = request.resolver_match.view_name
                if current_view not in EXEMPT_PATHS:
                    return redirect(reverse('accounts:user_info_create'))
        return self.get_response(request)
