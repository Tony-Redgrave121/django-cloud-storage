from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # id = models.BigAutoField(primary_key=True)
    # username = models.CharField(max_length=100, unique=True, null=False)
    # email = models.CharField(max_length=100, unique=True, null=False)
    # password = models.CharField(max_length=20, null=False)
    space = models.IntegerField(default=1024**3*10)
    used_space = models.IntegerField(default=0)

class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    access_link = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.ForeignKey('User', related_name='files', on_delete=models.CASCADE)
    parent_id = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
