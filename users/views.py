from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
import secrets
from django.contrib import messages

from config import settings
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    template_name = "register.html"
    success_url = reverse_lazy("users:login")
    fields = ["username", "email", "password", "avatar", "country"]

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/activate/{token}/'
        send_mail(
            subject = 'Подтверждение почты',
            message = f'Привет! Перейди по ссылке для подтверждения почты: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [user.email] )

        return super().form_valid(form)

def email_verification_user(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    user.token = None
    user.save()

    return redirect(reverse_lazy('users:login'))

class PasswordRecovery(FormView):
    model = CustomUser
    template_name = "password_recovery.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("sending:home")

    def form_valid(self, form):
        email = form.cleaned_data['email']

        try:
            #Ищем пользователя с таким email
            user = CustomUser.objects.get(email=email)
            if user.is_active:
                # Генерируем токен
                token = secrets.token_hex(16)
                user.token = token
                user.save()

                # Отправляем письмо
                host = self.request.get_host()
                url = f'http://{host}/users/password_recovery2/{token}/'
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Привет! Перейди по ссылке для восстановления пароля: {url}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
                messages.success(self.request, 'Ссылка для восстановления пароля отправлена на ваш email')
            else:
                messages.error(self.request, 'Аккаунт не активирован')
        except CustomUser.DoesNotExist:
            messages.error(self.request, 'Пользователь с таким email не найден')

        return super().form_valid(form)


def email_verification_user2(request, token):
    user = get_object_or_404(CustomUser, token=token, is_active=True)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.token = None
            user.is_active = True
            user.save()
            messages.success(request, 'Пароль успешно изменен! Теперь вы можете войти в систему.')
            return redirect('users:login')  # Перенаправляем на страницу входа
    else:
        form = SetPasswordForm(user)

    return render(request, 'password_recovery2.html', {'form': form, 'user': user})