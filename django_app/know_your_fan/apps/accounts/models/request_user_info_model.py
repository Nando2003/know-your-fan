import re
import datetime
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class RequestUserInfo(models.Model):
    STATUS_CHOICES = [
        ("validating", "Validando"),
        ("valid", "Válido"),
        ("invalid", "Inválido"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    unique_identifier = models.CharField(max_length=14)
    birth_date = models.DateField()

    task_id = models.UUIDField(default=uuid4, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="validating")

    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        from apps.accounts.models.user_info_model import UserInfo

        def validate_birth_date(birth_date: datetime.date):
            if birth_date is None:
                raise ValidationError({'birth_date': 'A data de nascimento não pode ser vazia'})
            if birth_date > datetime.date.today():
                raise ValidationError({'birth_date': 'A data de nascimento não pode ser futura'})

        def validate_unique_identifier(unique_identifier: str):
            if unique_identifier is None:
                raise ValidationError({'unique_identifier': 'O CPF não pode ser vazio'})

            unique_identifier = re.sub(r'\D', '', unique_identifier)

            if len(unique_identifier) != 11 or unique_identifier == unique_identifier[0] * 11:
                raise ValidationError({'unique_identifier': 'CPF inválido'})

            add = sum(int(unique_identifier[i]) * (10 - i) for i in range(9))
            digit1 = ((add * 10) % 11) % 10
            if digit1 != int(unique_identifier[9]):
                raise ValidationError({'unique_identifier': 'CPF inválido'})

            add = sum(int(unique_identifier[i]) * (11 - i) for i in range(10))
            digit2 = ((add * 10) % 11) % 10
            if digit2 != int(unique_identifier[10]):
                raise ValidationError({'unique_identifier': 'CPF inválido'})

            # Verifica se já foi cadastrado como UserInfo
            if UserInfo.objects.filter(unique_identifier=unique_identifier).exists():
                raise ValidationError({'unique_identifier': 'Este CPF já foi validado anteriormente.'})

        validate_birth_date(self.birth_date)
        validate_unique_identifier(self.unique_identifier)

    def save(self, *args, **kwargs):
        if self.status == "validating":
            self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Solicitação de {self.first_name} - {self.status}"
