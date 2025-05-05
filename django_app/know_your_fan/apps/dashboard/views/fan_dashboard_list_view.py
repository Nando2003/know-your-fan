from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.dashboard.models.dashboard_model import Dashboard


class DashboardListView(LoginRequiredMixin, ListView):
    model = Dashboard
    template_name = 'dashboard/dashboard_list.html'
    context_object_name = 'dashboards'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_info is None: # type: ignore
            return redirect("accounts:validation")

        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Dashboard.objects.filter(
            fan_profile__user_info__user=self.request.user
        ).order_by('-fan_profile__created_at')