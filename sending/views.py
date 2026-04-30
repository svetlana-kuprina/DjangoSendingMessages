from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from sending.forms import SendingMessageSendForm, SendingMessagesForm, SendingMessagesManForm
from sending.models import SendingMessages, Client, Message, MailingAttempts
from users.models import CustomUser


class HomeListView(ListView):
    model = SendingMessages
    template_name = "home.html"
    context_object_name = "sending_messages"

    # def get_queryset(self):
    #     """подсчет списка"""
    #     queryset = super().get_queryset()
    #     if not self.request.session.get('messages_list_viewed', False):
    #         self.request.session['messages_list_viewed'] = True
    #
    #     return queryset

    def get_context_data(self, **kwargs):
        """Подсчет списка со статусом "launched" и добавление значения в контекст """
        context = super().get_context_data(**kwargs)
        context['launched_count'] = self.object_list.filter(status="launched").count()
        context['total_clients_count'] = Client.objects.count()
        if self.request.user.is_authenticated:
            context['owner'] = CustomUser.objects.get(id=self.request.user.id)
        return context


class SendingMessagesListView(ListView):
    """Список рассылок"""
    model = SendingMessages
    template_name = "sending_messages.html"
    context_object_name = "sending_messages"


class SendingMessagesDetailView(LoginRequiredMixin, DetailView):
    """Просмотр рассылок"""
    model = SendingMessages
    template_name = "sending_message.html"
    context_object_name = "sending_message"


    def get_object(self, queryset=None):
        """Проверяем статус рассылки с помощью update_status в models"""
        """Проверка прав доступа"""
        obj = super().get_object(queryset)
        # Определяем имя приложения динамически
        app_label = self.model._meta.app_label
        manager_perm = f'{app_label}.manager'
        if obj.owner == self.request.user or self.request.user.has_perm(manager_perm):
            # изменение и сохранение статуса
            obj.update_status()
            return obj
        else:
            raise PermissionDenied("У вас нет прав для просмотра.")



    def get_context_data(self, **kwargs):
        """Подключаем форму подтверждения отправки сообщения"""
        context = super().get_context_data(**kwargs)
        context['send_form'] = SendingMessageSendForm()
        return context


class SendingMessageCreateView(LoginRequiredMixin, CreateView):
    """Добавление рассылок"""
    model = SendingMessages
    template_name = "sending_message_form.html"
    context_object_name = "sending_message"
    fields = ("start_time", "end_time", "status", "message", "client")
    success_url = reverse_lazy("sending:sending_messages")

    def form_valid(self, form):
        """Валидация формы ввода дат"""
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
        send_mess = form.save()
        user = self.request.user
        print(user)
        send_mess.owner = user
        response = super().form_valid(form)
        return response


class SendingMessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование рассылок"""
    model = SendingMessages
    template_name = "sending_message_form.html"
    context_object_name = "sending_message"

    success_url = reverse_lazy("sending:sending_messages")

    def get_form_class(self):
        """Проверка пользователь или менеджер"""
        user = self.request.user
        if user == self.object.owner:
            return SendingMessagesForm
        if user.has_perm("sending.manager"):
            return SendingMessagesManForm
        raise PermissionDenied


class SendingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление рассылок"""
    model = SendingMessages
    template_name = "sending_message_delete.html"
    context_object_name = "sending_message"
    success_url = reverse_lazy("sending:sending_messages")

    def has_permission(self):
        """Проверка прав доступа"""
        obj = self.get_object()
        return obj.owner == self.request.user


class ClientListView(ListView):
    """Список клиентов"""
    model = Client
    template_name = "clients.html"
    context_object_name = "clients"


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр клиентов"""
    model = Client
    template_name = "client.html"
    context_object_name = "client"


    def get_object(self, queryset=None):
        """Проверка прав доступа"""
        obj = super().get_object(queryset)
        # Определяем имя приложения динамически
        app_label = self.model._meta.app_label
        manager_perm = f'{app_label}.manager'
        if obj.owner == self.request.user or self.request.user.has_perm(manager_perm):
            return obj
        else:
            raise PermissionDenied("У вас нет прав для просмотра.")


class ClCreateView(LoginRequiredMixin, CreateView):
    """Создание клиентов"""
    model = Client
    template_name = "client_form.html"
    context_object_name = "client"
    fields = ("name", "email", "comment")
    success_url = reverse_lazy("sending:clients")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        return super().form_valid(form)


class ClUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование клиентов"""
    model = Client
    template_name = "client_form.html"
    context_object_name = "client"
    fields = ("name", "email", "comment", "owner")
    success_url = reverse_lazy("sending:clients")

    def has_permission(self):
        """Проверка прав доступа"""
        obj = self.get_object()
        return obj.owner == self.request.user


class ClDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление клиентов"""
    model = Client
    template_name = "client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("sending:clients")

    def has_permission(self):
        """Проверка прав доступа"""
        obj = self.get_object()
        return obj.owner == self.request.user


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

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "message_form.html"
    context_object_name = "message"
    fields = ("message_subject", "body", "owner")
    success_url = reverse_lazy("sending:messages")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("sending:messages")


class SendingMessageSendView(View):
    """View для отправки сообщения"""

    def post(self, request, pk):
        sending_message = get_object_or_404(SendingMessages, pk=pk)
        form = SendingMessageSendForm(request.POST)

        if form.is_valid():
            # Проверяем статус рассылки
            if sending_message.status != 'launched':
                messages.error(request, 'Рассылка не активна. Невозможно отправить сообщения.')
                MailingAttempts.objects.create(
                    sending_messages=sending_message,
                    status='Unsuccessful',
                    attempt_time=timezone.now(),
                    server_response='Рассылка не активна. Невозможно отправить сообщения.'
                )

                return redirect('sending:sending_message', pk=pk)

            # Проверяем время
            now = timezone.now()
            if now < sending_message.start_time:
                messages.error(request, f'Рассылка начнется {sending_message.start_time}. Сейчас отправка невозможна.')
                MailingAttempts.objects.create(
                    sending_messages=sending_message,
                    status='Unsuccessful',
                    attempt_time=timezone.now(),
                    server_response=f'Рассылка начнется {sending_message.start_time}. Сейчас отправка невозможна.'
                )
                return redirect('sending:sending_message', pk=pk)

            if now > sending_message.end_time:
                messages.error(request, 'Время рассылки истекло.')
                MailingAttempts.objects.create(
                    sending_messages=sending_message,
                    status='Unsuccessful',
                    attempt_time=timezone.now(),
                    server_response='Время рассылки истекло.'
                )
                return redirect('sending:sending_message', pk=pk)

            # Отправляем сообщения
            self.send_messages(sending_message, pk)

            return redirect('sending:sending_message', pk=pk)

    def send_messages(self, sending_message, pk):
        """Отправка сообщений клиентам"""
        subject = sending_message.message
        message = get_object_or_404(Message, pk=pk)
        recipient_list = [client.email for client in sending_message.client.all()]
        from_email = "kuprinasa@yandex.ru"
        try:

            # Отправка письма
            send_mail(subject, message.body, from_email, recipient_list)
            # Создаем запись о попытке отправки
            MailingAttempts.objects.create(
                sending_messages=sending_message,
                status='successful',
                attempt_time=timezone.now(),
                server_response=f'Письмо успешно отправлено {len(recipient_list)} получателю-(ям)'
            )

        except Exception as e:
            # Обновляем запись об ошибке
            MailingAttempts.objects.create(
                sending_messages=sending_message,
                status='Unsuccessful',
                attempt_time=timezone.now(),
                server_response=str(e)
            )


class StatisticsListView(LoginRequiredMixin, ListView):
    model = MailingAttempts
    template_name = "statistics.html"
    context_object_name = "statistics"

    def get_queryset(self):
        """Фильтруем записи, где owner = текущий пользователь"""
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        """Подсчет списка со статусом "launched" и добавление значения в контекст """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['owner'] = CustomUser.objects.get(id=self.request.user.id)
            if context['owner'] == self.request.user:
                context['Unsuccessful_count'] = self.object_list.filter(status="Unsuccessful").count()
                context['successful_count'] = self.object_list.filter(status="successful").count()

        return context
