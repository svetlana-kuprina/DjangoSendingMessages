from django.core.cache import cache

from sending.models import Message


def get_message_cached():
    message = cache.get("message_list")

    if message is None:
        message = Message.objects.all()
        cache.set("message_list", message,  60 * 15)

    return message