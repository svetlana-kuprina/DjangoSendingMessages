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
    status = models.CharField()