from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    ...

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
