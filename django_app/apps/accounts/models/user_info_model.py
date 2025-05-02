import re
import datetime
from django.db import models
from django.core.exceptions import ValidationError


class UserInfo(models.Model):
    user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    unique_identifier = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
    
    def clean(self):
        
        def validate_birth_date(birth_date: datetime.date):
            if birth_date > datetime.date.today():
                raise ValidationError({'birth_date': 'A data de nascimento não pode ser futura'})
        
        def validate_unique_identifier(unique_identifier: str):
            unique_identifier = re.sub(r'\D', '', self.unique_identifier)
            
            if len(unique_identifier) != 11 or unique_identifier == unique_identifier[0] * 11:
                raise ValidationError({'unique_identifier': 'CPF inválido'})
            
            add = sum(int(unique_identifier[i]) * (10 - i) for i in range(9))
            
            digit1 = ((add * 10) % 11) % 10
            if digit1 != int(unique_identifier[9]):
                raise ValidationError({'unique_identifier': 'CPF inválido'})
            
            add = sum(int(unique_identifier[i]) * (11 - i) for i in range(10))
            digit2 = ((add * 10) % 11) % 10
            if digit2 != int(unique_identifier[10]):
                raise ValidationError("CPF inválido.")
            
            self.unique_identifier = unique_identifier

        validate_birth_date(self.birth_date)
        validate_unique_identifier(self.unique_identifier)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)