from django.db import models
from apps.dashboard.models.game_model import Game
from apps.dashboard.models.team_model import Team
from apps.accounts.models.user_info_model import UserInfo


class FanProfile(models.Model):
    
    user_info = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        related_name='fan_profiles',
    )
    
    org_preference = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='fans',
        blank=False
    )
    
    games = models.ManyToManyField(
        Game,
        related_name='fans',
        blank=True,
        help_text="Selecione um ou mais jogos de interesse" 
    )
    
    rt_org_posts         = models.IntegerField(default=0)
    liked_org_posts      = models.IntegerField(default=0)  # ≥10 curtidas
    interacted_org_posts = models.IntegerField(default=0)  # ≥5 interações
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FanProfile"
        verbose_name_plural = "FanProfiles"
    
    @property
    def recent_purchases(self):
        """Compras do último ano."""
        from django.utils import timezone
        one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
        return self.purchases.filter(date__gte=one_year_ago) #type: ignore
    
    @property
    def recent_events(self):
        """Eventos/atividades do último ano."""
        from django.utils import timezone
        one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
        return self.events.filter(date__gte=one_year_ago) #type: ignore
    
    @property
    def events_count_last_year(self) -> int:
        """Número de eventos/atividades no último ano."""
        return self.recent_events.count()

    @property
    def purchases_count_last_year(self) -> int:
        """Número de compras no último ano."""
        return self.recent_purchases.count()
        
    def __str__(self):
        return f"{self.user_info.user.username} – Fan de {self.org_preference.name}"