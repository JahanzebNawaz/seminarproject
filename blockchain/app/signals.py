from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()


@receiver(post_save, sender=Customer)
def update_is_verified(sender, instance=None, created=False, **kwargs):
    if instance.is_verified:
        user = User.objects.get(pk=instance.user.pk)
        user.is_verified = True
        user.save()
