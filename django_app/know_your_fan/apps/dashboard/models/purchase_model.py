from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Purchase(models.Model):
    fan_profile = models.ForeignKey(
        'FanProfile',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    
    item = models.CharField(
        "Item Comprado",
        max_length=150,
        help_text="Descrição do produto ou serviço"
    )
    
    date = models.DateField(
        "Data da Compra",
        help_text="Data em que a compra foi realizada"
    )
    
    cost = models.DecimalField(
        "Valor (R$)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True,
        help_text="Valor gasto (opcional)"
    )

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.item} — R${self.cost or '0.00'} em {self.date}"

    def clean(self):
        qs = Purchase.objects.filter(fan_profile=self.fan_profile)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count() >= 10:
            raise ValidationError("Você já atingiu o limite de 10 compras para este perfil.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    