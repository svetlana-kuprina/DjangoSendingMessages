from django.urls import path
from sending.apps import SendingConfig
from sending.views import SendingMessagesListView, ClientListView, MessageListView, SendingMessagesDetailView, \
    HomeListView, ClientDetailView, ClCreateView, ClUpdateView, ClDeleteView, MessageDetailView, MessageDeleteView, \
    MessageCreateView, MessageUpdateView, SendingMessageUpdateView, SendingMessageDeleteView, SendingMessageCreateView

app_name = SendingConfig.name

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("sending_messages/", SendingMessagesListView.as_view(), name="sending_messages"),
    path("sending_message/<int:pk>/", SendingMessagesDetailView.as_view(), name="sending_message"),
    path("sending_message_create/", SendingMessageCreateView.as_view(), name="sending_message_create"),
    path("sending_message_delete/<int:pk>/", SendingMessageDeleteView.as_view(), name="sending_message_delete"),
    path("sending_message_update/<int:pk>/", SendingMessageUpdateView.as_view(), name="sending_message_update"),
    path("clients/", ClientListView.as_view(), name="clients"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client"),
    path("client_create/", ClCreateView.as_view(), name="client_create"),
    path("client_update/<int:pk>/", ClUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>/",ClDeleteView.as_view(), name="client_delete"),
    path("messages/", MessageListView.as_view(), name="messages"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
]
