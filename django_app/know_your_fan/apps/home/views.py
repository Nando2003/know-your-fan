from typing import Any
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse as HttpResponse


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home/home.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.user_info is not None: # type: ignore
            return redirect("accounts:validation")
        return super().dispatch(request, *args, **kwargs)