from django.db import models
from django.contrib.auth.models import User


class UserModel(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    bio     = models.CharField(max_length=30, blank=True, null=True)
    image   = models.ImageField(blank=True, null=True, upload_to="uploads")
    address = models.CharField(max_length=100, blank=True, null=True)
    phone   = models.BigIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['pk']
        verbose_name = 'User'
        verbose_name_plural = 'Users'