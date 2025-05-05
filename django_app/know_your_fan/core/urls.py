from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.home.urls')),
    
    path('accounts/', include('apps.accounts.urls')),
    
    path('dashboard/', include('apps.dashboard.urls')),
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]