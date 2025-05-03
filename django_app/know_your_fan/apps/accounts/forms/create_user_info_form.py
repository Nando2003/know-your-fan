from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from apps.accounts.models.user_info_model import UserInfo


def validate_image_extension(image: UploadedFile):
    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError("Envie uma imagem JPG ou PNG.")
    

class UserInfoCreateForm(forms.ModelForm):
    
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data de nascimento',
        required=True,
    )
    
    rg_front = forms.ImageField(
        required=True,
        validators=[validate_image_extension],
        help_text="Envie a frente do RG (JPG ou PNG).",
    )
    rg_back = forms.ImageField(
        required=True,
        validators=[validate_image_extension],
        help_text="Envie o verso do RG (JPG ou PNG).",
    )
    
    class Meta:
        model = UserInfo
        
        fields = (
            'first_name', 
            'last_name', 
            'unique_identifier', 
            'birth_date'
        )
        
        # help_texts = {
        #     'first_name': 'Seu primeiro nome (sem abreviações).',
        #     'unique_identifier': 'Digite seu CPF sem pontos ou traço.',
        # }

