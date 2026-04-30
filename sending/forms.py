from django import forms
from django.db.models import Model

from sending.models import SendingMessages


class SendingMessageSendForm(forms.Form):
    confirm_send = forms.BooleanField(
        label='Подтверждение отправки',
        required=True,
        help_text='Подтвердите, что хотите отправить рассылку'
    )

class SendingMessagesManForm(forms.ModelForm):
    """Форма для менеджера"""
    class Meta:
        model = SendingMessages
        fields = ('status',)

class SendingMessagesForm(forms.ModelForm):
    """Форма для менеджера"""
    class Meta:
        model = SendingMessages
        fields = ("start_time", "end_time", "status", "message", "client", "owner")