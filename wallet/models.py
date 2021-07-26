from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models.signals import post_save
import binascii
from accounts.models import Profile
import random 
import os 
import string 

def generate_wallet_id():
    while True:
        _id = binascii.b2a_hex(os.urandom(7))
        if Wallet.objects.filter(wallet_id=_id).count() == 0:
            break 

    return _id 


def generate_transaction_id():
    while True:
        trx_id = binascii.b2a_hex(os.urandom(14))
        if Transaction.objects.filter(transaction_id=trx_id).count() == 0:
            break 

    return trx_id 

# Create your models here.
class Wallet(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=17, validators=[MinLengthValidator(17), MaxLengthValidator(17)], default=generate_wallet_id, unique=True)
    is_disabled = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self) :
        return self.account.email


class Transaction(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)], default=generate_transaction_id)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    to = models.CharField(max_length=60)

    def __str__(self):
        return self.account.email 


class Payment(models.Model):
    from_acct = models.ForeignKey(Profile, on_delete=models.CASCADE)
    to_acct = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.from_acct.email 






    