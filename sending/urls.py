from django.urls import path
from sending.apps import SendingConfig

app_name = SendingConfig.name

#TODO "доделать пути к шаблонам"
# urlpatterns = [
#     path("", SendingListView.as_view(), name="home"),
# ]