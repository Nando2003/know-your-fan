from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
