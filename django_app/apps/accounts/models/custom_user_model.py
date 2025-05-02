from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    user_info = models.OneToOneField("accounts.UserInfo", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def __str__(self):
        return self.username
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )