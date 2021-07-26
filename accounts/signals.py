from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .models import Profile
from wallet.models import Wallet

@receiver(post_save, sender=Profile)
def create_wallet(sender, created, instance, *args, **kwargs):
    if created:
        Wallet.objects.create(account=instance)