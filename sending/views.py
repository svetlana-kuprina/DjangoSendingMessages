from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from sending.models import SendingMessages


class SendingMessagesListView(ListView):
    model = SendingMessages
    template_name = "home.html"
    context_object_name = "sending_messages"

class SendingMessagesDetailView(DetailView):
    model = SendingMessages
    template_name = "home.html"
    context_object_name = "sending_message"

