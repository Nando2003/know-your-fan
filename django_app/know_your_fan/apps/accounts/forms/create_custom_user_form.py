from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models.custom_user_model import CustomUser


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email')
        
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', 'A nova senha e a confirmação não correspondem.')

        return cleaned_data
        
    