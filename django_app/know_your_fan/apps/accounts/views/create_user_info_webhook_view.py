import re
import json
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.accounts.models.user_info_model import UserInfo
from apps.accounts.models.request_user_info_model import RequestUserInfo

@csrf_exempt
@require_POST
def validation_webhook_view(request: HttpRequest) -> JsonResponse:
    token = request.headers.get("X-WEBHOOK-TOKEN", None)
    if token != settings.X_WEBHOOK_TOKEN:
        return JsonResponse({"error": "Token inválido"}, status=403)

    try:
        data = json.loads(request.body)
        task_id = data.get("task_id")
        rg_front = data.get("rg_front", "").lower()
        rg_back = data.get("rg_back", "").lower()

        if not task_id or not rg_front or not rg_back:
            return JsonResponse({"error": "Dados incompletos"}, status=400)

        try:
            request_info = RequestUserInfo.objects.get(task_id=task_id)
        except RequestUserInfo.DoesNotExist:
            return JsonResponse({"error": "Task ID não encontrado"}, status=404)

        if request_info.status != "validating":
            return JsonResponse({"error": f"Solicitação já processada: {request_info.status}"}, status=409)

        # Normaliza e valida dados
        normalized_cpf = re.sub(r"\D", "", request_info.unique_identifier)
        cpf_found = normalized_cpf in re.sub(r"\D", "", rg_back)
        
        name = request_info.first_name.lower()
        name_found = name in rg_front or name in rg_back

        # Se dados validados corretamente
        if name_found and cpf_found:
            
            # Verifica se o CPF já está em uso em outra conta
            if UserInfo.objects.filter(unique_identifier=normalized_cpf).exists():
                request_info.status = "invalid"
                request_info.save()
                return JsonResponse({"status": "invalid", "error": "CPF já cadastrado"})

            if not getattr(request_info.user, "user_info", None):
                user_info = UserInfo(
                    user=request_info.user,
                    first_name=request_info.first_name,
                    last_name=request_info.last_name,
                    birth_date=request_info.birth_date,
                    unique_identifier=normalized_cpf,
                )
                user_info.full_clean()
                user_info.save()

            request_info.status = "valid"
        else:
            request_info.status = "invalid"

        request_info.save()
        return JsonResponse({"status": request_info.status})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
