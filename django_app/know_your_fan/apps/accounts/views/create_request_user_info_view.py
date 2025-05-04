import httpx
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from asgiref.sync import async_to_sync
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.accounts.models.request_user_info_model import RequestUserInfo
from apps.accounts.forms.create_request_user_info_form import RequestUserInfoCreateForm


@async_to_sync
async def send_to_ocr(front_bytes, back_bytes, front_type, back_type):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://fastapi_app:8001/upload-rg/",
            files={
                "rg_front": ("rg_front.png", front_bytes, front_type),
                "rg_back": ("rg_back.png", back_bytes, back_type),
            },
            timeout=120.0
        )
        response.raise_for_status()
        return response


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class CreateRequestUserInfoView(CreateView):
    form_class = RequestUserInfoCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/create_request_user_info.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        last_request = RequestUserInfo.objects.filter(user=user).order_by('-created_at').first()

        if last_request:
            if last_request.status == "validating":
                return redirect("accounts:waiting_validation")

            elif last_request.status == "valid":
                return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)

    
    def form_valid(self, form):
        user = self.request.user
        request_user_info: RequestUserInfo = form.save(commit=False)
        request_user_info.user = user

        rg_front_file = self.request.FILES.get('rg_front')
        rg_back_file = self.request.FILES.get('rg_back')

        if not (rg_front_file and rg_back_file):
            form.add_error(None, "Please upload both front and back of your ID.")
            return self.form_invalid(form)

        front_bytes = rg_front_file.read()
        back_bytes = rg_back_file.read()
 
        try:
            response = send_to_ocr(front_bytes, back_bytes, rg_front_file.content_type, rg_back_file.content_type)

            if response.status_code == 200:
                task_id_data = response.json()
                task_id = task_id_data.get("task_id", "")
                
                if not task_id:
                    form.add_error(None, "Erro ao processar o RG")
                    return self.form_invalid(form)
                
                request_user_info.task_id = task_id
                request_user_info.save()
                
                messages.success(self.request, "Pedido de validação enviado!")
                return super().form_valid(form)

            else:
                form.add_error(None, "Erro no serviço de OCR")
                return self.form_invalid(form)

        except httpx.RequestError as _:
            form.add_error(None, "Erro de rede com o OCR")
            return self.form_invalid(form)
