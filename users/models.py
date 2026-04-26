from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email")

    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    telephone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True, help_text="Введите номер телефона"
    )
    country = models.CharField(max_length=50, verbose_name="Страна", null=True, blank=True, help_text="Введите страну")
    token = models.CharField(max_length=100, unique=True, verbose_name='Token', null=True, blank=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email