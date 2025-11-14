from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'custom_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
