from django.urls import path
from sending.apps import SendingConfig
from sending.views import SendingMessagesListView

app_name = SendingConfig.name


urlpatterns = [path("", SendingMessagesListView.as_view(), name="home"),]