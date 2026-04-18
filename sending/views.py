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



class MessageListView(ListView):
    model = Message
    template_name = "messages.html"
    context_object_name = "messages"
