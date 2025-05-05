import datetime
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.accounts.models.request_user_info_model import RequestUserInfo


@login_required
def check_validation_status_view(request):
    request_info = RequestUserInfo.objects.filter(
        user=request.user).order_by('-created_at').first()

    if not request_info:
        return JsonResponse({"status": "none"}, status=200)

    elapsed = now() - request_info.created_at
    
    if request_info.status == "validating":
        
        if elapsed > datetime.timedelta(minutes=2, seconds=30):
            
            request_info.status = "invalid"
            request_info.save()
    
    return JsonResponse({"status": request_info.status})
