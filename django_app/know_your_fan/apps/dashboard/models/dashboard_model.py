from django.db import models
from apps.dashboard.models.fan_profile_model import FanProfile


class Dashboard(models.Model):
    choices=[
        ('loading', 'Carregando'),
        ('finished', 'Finalizado')
    ]
    
    twitter_status = models.CharField(
        max_length=20,
        choices=choices,
        default='loading',
    )
    
    news_status = models.CharField(
        max_length=20,
        choices=choices,
        default='loading',
    )
    
    fan_profile = models.ForeignKey(
        FanProfile,
        on_delete=models.CASCADE,
        related_name='fan_dashboards'
    )
    
    news = models.ManyToManyField(
        'ESportsNews',
        related_name='dashboards'
    )
    
    # score = models.IntegerField(default=0)
    
    # def calculate_score(self):
    #     fp = self.fan_profile
        
    #     events_points    = fp.events_count_last_year * 4
    #     purchases_points = fp.purchases_count_last_year * 4

    #     twitter_points = 0
        
    #     if fp.rt_org_posts:
    #         twitter_points += 10
    #     if fp.liked_org_posts:
    #         twitter_points += 10
    #     if fp.interacted_org_posts:
    #         twitter_points += 16

    #     return events_points + purchases_points + twitter_points
    
    # def save(self, *args, **kwargs):
    #     self.score = self.calculate_score()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Dashboard #{self.pk}"