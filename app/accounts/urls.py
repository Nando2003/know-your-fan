from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [

    path(
        'accounts/login/', auth_views.LoginView.as_view(
            redirect_authenticated_user=True, template_name='registration/login.html'), 
            name='login'
    ),
    
    path(
        'accounts/logout/', auth_views.LogoutView.as_view(
            next_page='/accounts/login/'), 
            name='logout'
    ),
    
]