from django.contrib import admin
from . import models 

# Register your models here.
@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["account", "wallet_id", "is_disabled", "balance"]
    list_editable = ["is_disabled", "balance"]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "transaction_id", "amount", "timestamp", "to"]