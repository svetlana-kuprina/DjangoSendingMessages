
from django.utils import timezone

from django.db import models

from users.models import CustomUser


class Client(models.Model):
    """Модель: получатель рассылки (клиент)"""

    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="email")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарии")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="owner_client", verbose_name="Владелец", blank=True, null=True
    )

    def __str__(self):
        return f"Адрес эл. почты: {self.email}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["email"]
        permissions = [("manager", "Manager")]


class Message(models.Model):
    """Модель: сообщение"""

    message_subject = models.CharField(max_length=150, null=True, blank=True, verbose_name="Тема письма")
    body = models.TextField(null=True, blank=True, verbose_name="Тело письма")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="owner_message", verbose_name="Владелец", blank=True, null=True
    )

    def __str__(self):
        return self.message_subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["message_subject"]


class SendingMessages(models.Model):
    """Модель: рассылка"""

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('paused', 'Приостановлена'),
        ('completed', 'Завершена'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='sending_messages',
                                verbose_name="Сообщение")
    client = models.ManyToManyField(Client, verbose_name="Клиент")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="owner_sendingmessages", verbose_name="Владелец", blank=True, null=True
    )

    def __str__(self):
        return f"Сообщение:{self.message} Клиент:{self.client} Статус:{self.status}"

    def update_status(self):
        now_data = timezone.now()
        if now_data < self.start_time:
            self.status = 'created'
        if self.start_time < now_data < self.end_time:
            self.status = "launched"
            self.save()
        elif now_data > self.end_time:
            self.status = "completed"
            self.save()
        else:
            self.status = "created"
            self.save()



    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["message"]
        permissions = [("manager", "Manager")]


class MailingAttempts(models.Model):
    """Модель: попытки рассылок"""

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('Unsuccessful', 'Неуспешно'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(null=True, blank=True, verbose_name="Ответ почтового сервера")
    sending_messages = models.ForeignKey(SendingMessages, on_delete=models.DO_NOTHING, related_name='sending_messages',
                                         verbose_name="Рассылка сообщений")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="owner_mailingattempts", verbose_name="Владелец", blank=True, null=True
    )

    def __str__(self):
        return f"Рассылка:{self.sending_messages} Дата отправки:{self.attempt_time} Статус:{self.status}"

    class Meta:
        verbose_name = "Попытка рассылок"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_time"]
