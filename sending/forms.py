from django import forms
from .models import SendingMessages
#TODO Черновик надо исправить
class SendingMessageSendForm(forms.Form):
    confirm_send = forms.BooleanField(
        label='Подтверждение отправки',
        required=True,
        help_text='Подтвердите, что хотите отправить рассылку'
    )