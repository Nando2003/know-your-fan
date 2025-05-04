from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from apps.accounts.forms.create_custom_user_form import CustomUserCreateForm


class CreateCustomUserView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        
        return super().dispatch(request, *args, **kwargs)