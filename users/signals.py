from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    send_mail(
        'Sender Example',
        f'Hello {instance.username}, welcome goodreads.com. Read books and anjoy it!',
        'xoliqberdiyevbehruz6@gmail.com',
        [instance.email]
    )
