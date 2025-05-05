from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import Http404

from apps.dashboard.models.dashboard_model import Dashboard


class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = Dashboard
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'dashboard'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_info is None:  # type: ignore
            return redirect("accounts:validation")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Dashboard.objects.filter(
            fan_profile__user_info__user=self.request.user,
            news_status='finished'
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.fan_profile.user_info.user != self.request.user:
            raise Http404("Dashboard não encontrado.")
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        fp = self.object.fan_profile  # type: ignore

        events_points    = fp.events_count_last_year * 4
        purchases_points = fp.purchases_count_last_year * 4
        twitter_points = (
            fp.rt_org_posts         * 10 +
            fp.liked_org_posts      * 10 +
            fp.interacted_org_posts * 16
        )

        ctx['score'] = events_points + purchases_points + twitter_points
        return ctx

