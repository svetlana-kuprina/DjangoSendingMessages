from django import forms


class SendingMessageSendForm(forms.Form):
    confirm_send = forms.BooleanField(
        label='Подтверждение отправки',
        required=True,
        help_text='Подтвердите, что хотите отправить рассылку'
    )