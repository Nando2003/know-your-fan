from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.accounts.forms.create_user_info_form import UserInfoCreateForm


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class CreateUserInfoView(CreateView):
    form_class = UserInfoCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/create_user_info.html'