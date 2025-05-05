from django.db import models
from django.core.exceptions import ValidationError


class FanEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('LAN Party', 'LAN Party'),
        ('Torneio', 'Torneio'),
        ('Meetup', 'Meetup'),
        ('Stream', 'Stream'),
        ('Viewing Party', 'Viewing Party'),
        ('Torcida Organizada', 'Torcida Organizada'),
        ('Workshop', 'Workshop'),
        ('Lançamento de Jogo', 'Lançamento de Jogo'),
        ('Torneio Online', 'Torneio Online'),
        ('Campeonato Internacional', 'Campeonato Internacional'),
    ]
    
    fan_profile = models.ForeignKey(
        'FanProfile',
        on_delete=models.CASCADE,
        related_name='events'
    )
    
    date = models.DateField(
        "Data do Evento",
        help_text="Data em que o evento ou atividade ocorreu"
    )
    
    event_type = models.CharField(
        "Tipo de Evento",
        max_length=30,
        choices=EVENT_TYPE_CHOICES
    )
    
    description = models.CharField(
        "Descrição",
        max_length=255,
        help_text="Breve texto sobre o que aconteceu"
    )

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date}: {self.event_type}"
    
    def clean(self):
        # Conta quantos eventos já existem (exclui o próprio, se for edição)
        qs = FanEvent.objects.filter(fan_profile=self.fan_profile)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count() >= 10:
            raise ValidationError("Você já atingiu o limite de 10 eventos para este perfil.")
    
    def save(self, *args, **kwargs):
        # Garante que clean() seja chamado antes de salvar
        self.full_clean()
        super().save(*args, **kwargs)