from tkinter.constants import CASCADE

from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="email")
    comment = models.TextField(null=True, blank=True, verbose_name="Коментарии")

    def __str__(self):
        return f"ФИО: {self.name} Адрес эл. почты: {round(self.email)} Комментарий: [{self.comment}]"


    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["email"]


class Message(models.Model):
    message_subject = models.CharField(max_length=150, null=True, blank=True, verbose_name="Тема письма")
    body = models.TextField(null=True, blank=True, verbose_name="Тело письма")

    def __str__(self):
        return self.message_subject
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["message_subject"]


class SendingMessages(models.Model):
    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='sending_messages', verbose_name="Сообщение")
    client = models.ManyToManyField(Client, verbose_name="Клиент")

    def __str__(self):
        return f"Сообщение:{self.message} Клиент:{self.client} Статус:{self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["message"]

class MailingAttempts(models.Model):
    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('Unsuccessful', 'Неуспешно'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.CharField(null=True, blank=True, verbose_name="Ответ почтового сервера")
    sending_messages = models.ForeignKey(SendingMessages, on_delete=models.DO_NOTHING, related_name='sending_messages', verbose_name="Рассылка сообщений")

    def __str__(self):
        return f"Рассылка:{self.sending_messages} Дата отправки:{self.start_time} Статус:{self.status}"
    class Meta:
        verbose_name = "Попытка рассылок"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["start_time"]