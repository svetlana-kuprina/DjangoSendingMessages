from django.urls import path
from sending.apps import SendingConfig
from sending.views import SendingMessagesListView, ClientListView, MessageListView, SendingMessagesDetailView, \
    HomeListView, ClientDetailView, ClCreateView

app_name = SendingConfig.name

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("sending_messages/", SendingMessagesListView.as_view(), name="sending_messages"),
    path("sending_message/<int:pk>/", SendingMessagesDetailView.as_view(), name="sending_message"),
    path("clients/", ClientListView.as_view(), name="clients"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client"),
    path("client_сreate/<int:pk>/", ClCreateView.as_view(), name="client_create"),
    path("messages/", MessageListView.as_view(), name="messages"),
]
