from rest_framework import serializers
from . import models 


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ("wallet_id", "is_disabled", "balance")
        extra_kwargs = {
            "wallet_id": {
                "read_only": True
            },

            "is_disabled": {
                "read_only": True
            },

            "balance": {
                "read_only": True
            }
        }


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ("transaction_id", "amount", "timestamp", "to")
        extra_kwargs = {
            "transaction_id": {
                "read_only": True
            },

            "amount": {
                "read_only": True
            }, 

            "timestamp": {
                "read_only": True
            },

            "to": {
                "read_only": True 
            }
        }
        

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ("to_acct", "amount", )
        
        