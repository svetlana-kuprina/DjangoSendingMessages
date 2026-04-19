from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from config import settings
from sending.forms import SendingMessageSendForm
from sending.models import SendingMessages, Client, Message


class HomeListView(ListView):
    model = SendingMessages
    template_name = "home.html"
    context_object_name = "sending_messages"

    def get_queryset(self):
        """подсчет списка"""
        queryset = super().get_queryset()
        if not self.request.session.get('messages_list_viewed', False):
            self.request.session['messages_list_viewed'] = True

        return queryset

    def get_context_data(self, **kwargs):
        """Подсчет списка со статусом "launched" и добавление значения в контекст """
        context = super().get_context_data(**kwargs)
        context['launched_count'] = self.object_list.filter(status="launched").count()
        context['total_clients_count'] = Client.objects.count()
        return context


class SendingMessagesListView(ListView):
    model = SendingMessages
    template_name = "sending_messages.html"
    context_object_name = "sending_messages"


class SendingMessagesDetailView(DetailView):
    model = SendingMessages
    template_name = "sending_message.html"
    context_object_name = "sending_message"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['send_form'] = SendingMessageSendForm()
        return context


class SendingMessageCreateView(CreateView):
    model = SendingMessages
    template_name = "sending_message_form.html"
    context_object_name = "sending_message"
    fields = ("start_time", "end_time", "status", "message", "client")
    success_url = reverse_lazy("sending:sending_messages")

    def form_valid(self, form):
        now_time = timezone.now()
        start_time = form.instance.start_time
        end_time = form.instance.end_time

        # Проверка 1: Дата начала не может быть в прошлом
        if start_time < now_time:
            form.add_error('start_time', 'Дата и время начала не могут быть в прошлом')
            return self.form_invalid(form)

        # Проверка 2: Дата окончания должна быть позже даты начала
        if end_time <= start_time:
            form.add_error('end_time', 'Дата и время окончания должны быть позже даты начала')
            return self.form_invalid(form)
        # Если все проверки пройдены
        response = super().form_valid(form)
        return response


class SendingMessageUpdateView(UpdateView):
    model = SendingMessages
    template_name = "sending_message_form.html"
    context_object_name = "sending_message"
    fields = ("start_time", "end_time", "status", "message", "client")
    success_url = reverse_lazy("sending:sending_messages")


class SendingMessageDeleteView(DeleteView):
    model = SendingMessages
    template_name = "sending_message_delete.html"
    context_object_name = "sending_message"
    success_url = reverse_lazy("sending:sending_messages")


class ClientListView(ListView):
    model = Client
    template_name = "clients.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client.html"
    context_object_name = "client"


class ClCreateView(CreateView):
    model = Client
    template_name = "client_form.html"
    context_object_name = "client"
    fields = ("name", "email", "comment")
    success_url = reverse_lazy("sending:clients")


class ClUpdateView(UpdateView):
    model = Client
    template_name = "client_form.html"
    context_object_name = "client"
    fields = ("name", "email", "comment")
    success_url = reverse_lazy("sending:clients")


class ClDeleteView(DeleteView):
    model = Client
    template_name = "client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("sending:clients")


class MessageListView(ListView):
    model = Message
    template_name = "messages.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "message.html"
    context_object_name = "message"


class MessageCreateView(CreateView):
    model = Message
    template_name = "message_form.html"
    context_object_name = "message"
    fields = ("message_subject", "body")
    success_url = reverse_lazy("sending:messages")


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "message_form.html"
    context_object_name = "message"
    fields = ("message_subject", "body")
    success_url = reverse_lazy("sending:messages")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("sending:messages")

#TODO Черновик надо исправить
class SendingMessageSendView(View):
    """View для отправки сообщения"""

    def post(self, request, pk):
        sending_message = get_object_or_404(SendingMessages, pk=pk)
        form = SendingMessageSendForm(request.POST)

        if form.is_valid():
            # Проверяем статус рассылки
            if sending_message.status != 'launched':
                messages.error(request, 'Рассылка не активна. Невозможно отправить сообщения.')
                return redirect('sending:sending_message', pk=pk)

            # Проверяем время
            now = timezone.now()
            if now < sending_message.start_time:
                messages.error(request, f'Рассылка начнется {sending_message.start_time}. Сейчас отправка невозможна.')
                return redirect('sending:sending_message', pk=pk)

            if now > sending_message.end_time:
                messages.error(request, 'Время рассылки истекло.')
                return redirect('sending:sending_message', pk=pk)

            # Отправляем сообщения
            result = self.send_messages(sending_message)

            if result['success']:
                messages.success(request,
                                 f'Сообщения успешно отправлены! Отправлено: {result["sent"]}, Ошибок: {result["failed"]}')
            else:
                messages.error(request, f'Ошибка при отправке: {result["error"]}')

            return redirect('sending:sending_message', pk=pk)
        else:
            messages.error(request, 'Пожалуйста, подтвердите отправку.')
            return redirect('sending:sending_message', pk=pk)

    def send_messages(self, sending_message):
        """Отправка сообщений клиентам"""
        message_obj = sending_message.message
        clients = sending_message.client.all()

        if not clients.exists():
            return {'success': False, 'error': 'Нет получателей для рассылки'}

        sent_count = 0
        failed_count = 0
        failed_emails = []

        # Получаем тему и текст сообщения
        subject = message_obj.title  # или другой заголовок
        text_content = message_obj.body  # Текстовое содержимое
        html_content = message_obj.body_html if hasattr(message_obj,
                                                        'body_html') else None  # HTML содержимое (опционально)

        from_email = settings.DEFAULT_FROM_EMAIL

        for client in clients:
            try:
                if not client.email:
                    failed_count += 1
                    failed_emails.append(f"Клиент {client.id}: нет email")
                    continue

                # Персонализация сообщения
                personalized_text = text_content
                personalized_html = html_content

                # Заменяем плейсхолдеры на данные клиента
                personalized_text = personalized_text.replace('{{client_name}}',
                                                              client.name if client.name else 'Клиент')
                personalized_html = personalized_html.replace('{{client_name}}',
                                                              client.name if client.name else 'Клиент') if personalized_html else None

                if html_content:
                    # Отправка HTML письма
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=personalized_text,
                        from_email=from_email,
                        to=[client.email],
                    )
                    email.attach_alternative(personalized_html, "text/html")
                    email.send()
                else:
                    # Отправка обычного текстового письма
                    send_mail(
                        subject=subject,
                        message=personalized_text,
                        from_email=from_email,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )

                sent_count += 1

            except Exception as e:
                failed_count += 1
                failed_emails.append(f"{client.email}: {str(e)}")

        # Обновляем статус рассылки, если отправлены все сообщения
        if sent_count > 0:
            sending_message.sent_at = timezone.now()
            sending_message.save()

        result = {
            'success': sent_count > 0,
            'sent': sent_count,
            'failed': failed_count,
            'failed_details': failed_emails
        }

        return result