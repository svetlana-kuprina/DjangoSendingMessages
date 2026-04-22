from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    template_name = "register.html"
    success_url = reverse_lazy("users:login")
    fields = ["email", "username", "password", "avatar", "telephone", "country"]




