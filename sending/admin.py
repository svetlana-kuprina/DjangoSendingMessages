from django.contrib import admin

from .models import Client, Message, SendingMessages, MailingAttempts


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "comment")
    list_filter = ("email",)
    search_fields = (
        "name",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "message_subject")


@admin.register(SendingMessages)
class SendingMessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "status")
    list_filter = ("client",)


@admin.register(MailingAttempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "status")
