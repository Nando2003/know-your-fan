from django.urls import path
from apps.dashboard.views.news_webhook_view import news_webhook_view
from apps.dashboard.views.twitter_views import twitter_login, twitter_callback, twitter_ready
from apps.dashboard.views.create_fan_profile_view import CreateFanProfileView
from apps.dashboard.views.fan_dashboard_list_view import DashboardListView
from apps.dashboard.views.fan_dashboard_detail_view import DashboardDetailView

app_name = "dashboard"

urlpatterns = [
    path('create/', CreateFanProfileView.as_view(), name='dashboard_create'),
    path('list/', DashboardListView.as_view(), name='dashboard_list'),
    
    path('twitter/login/', twitter_login, name='twitter_login'),
    path('twitter/callback/', twitter_callback, name='twitter_callback'),
    path('twitter/ready/',    twitter_ready,    name='twitter_ready'),
    
    path('webhook/', news_webhook_view, name='news_webhook'),
    
    path('<int:pk>/', DashboardDetailView.as_view(), name='dashboard_detail'),
]
