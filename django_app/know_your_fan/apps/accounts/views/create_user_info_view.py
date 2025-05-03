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
    
    # def form_valid(self, form):
    #     user = self.request.user
        
    #     user_info: UserInfo = form.save(commit=False)
    #     user_info.user = user

    #     rg_front = self.request.FILES.get('rg_front')
    #     rg_back = self.request.FILES.get('rg_back')

    #     if not (rg_back and rg_front):
    #         form.add_error(None, "Envie a frente e o verso do RG.")
    #         return self.form_invalid(form)
        
    #     front_bytes = rg_front.read()
    #     back_bytes = rg_back.read()
        
    #     user_info.save()
        
    #     return super().form_valid(form)