from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class WaitingValidationView(TemplateView):
    template_name = 'accounts/waiting_validation.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_info is not None: # type: ignore
            return redirect("home:home")
        
        return super().dispatch(request, *args, **kwargs)
