from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

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
