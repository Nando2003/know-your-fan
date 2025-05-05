from django.db import models
from django.contrib.postgres.fields import ArrayField


class Team(models.Model):
    name = models.CharField(max_length=120)
    logo = models.URLField()
    x_account = models.URLField()
    
    keywords = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
    )
    
    def all_labels(self):
        """
        Retorna a lista de labels para análise zero-shot ou keyword matching,
        incluindo o próprio nome.
        """
        return [self.name] + self.keywords
    
    def __str__(self):
        return self.name