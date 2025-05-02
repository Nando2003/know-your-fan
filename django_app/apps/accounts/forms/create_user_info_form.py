from django import forms
from apps.accounts.models.user_info_model import UserInfo


class UserInfoCreateForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        
        fields = (
            'first_name', 
            'last_name', 
            'unique_identifier', 
            'birth_date'
        )