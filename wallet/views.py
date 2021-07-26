from rest_framework.generics import ListCreateAPIView, ListAPIView
from accounts.models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from . import serializers
from . import models

# Create your views here.
class AccountWalletView(APIView):
    serializer_class = serializers.WalletSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet_data = models.Wallet.objects.filter(
            account=request.user).values()[0]

        if wallet_data["is_disabled"] == True:
            return Response({
                "account status": "blocked",
                "wallet id": wallet_data['wallet_id'],
                "message": "Your account has been disabled, contact support"
            })

        else:
            return Response({
                "account status": "enabled",
                "wallet id": wallet_data['wallet_id'],
                "balance": float(wallet_data['balance'])
            })


class SuccessView(APIView):
    def get(self, request):
        return Response({
            "message": "Transfer Complete! Head back home http://0.0.0.0:8000/api/my-wallet/"
        }, status=status.HTTP_200_OK)


class TransactionsListView(ListAPIView):
    serializer_class = serializers.TransactionHistorySerializer
    queryset = models.Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        account_transactions = models.Transaction.objects.filter(account=self.request.user)
        serializer = serializers.TransactionHistorySerializer(account_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakePaymentView(APIView):
    serializer_class = serializers.PaymentSerializer

    def get(self, request, format=None):
        message = "Start sending money by just typing in a username!"
        return Response({
            "message": message
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            val_data = dict(serializer.validated_data)

            if Profile.objects.filter(username=val_data['to_acct']).count() == 1:
                if val_data['to_acct'] == request.user.username:
                    return Response({
                        "alert": "You can't send money to yourself silly!"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    amount = val_data['amount']
                    sender_acct = models.Wallet.objects.get(account=self.request.user)
                    recv_account = Profile.objects.get(username=val_data['to_acct'])
                    wallet_instance = models.Wallet.objects.get(account=recv_account)

                    if float(amount) > float(sender_acct.balance):
                        return Response({
                            'alert': "You do not have enough funds to complete the transfer..."
                        }, status=status.HTTP_406_NOT_ACCEPTABLE)

                    else:
                        wallet_instance.balance = float(wallet_instance.balance) + float(amount)
                        wallet_instance.save()

                        sender_acct.balance = float(sender_acct.balance) - float(val_data['amount'])
                        sender_acct.save()

                        trx = models.Transaction.objects.create(
                            account = request.user,
                            amount = amount,
                            to = val_data['to_acct']
                        )

                        trx.save()
                        return redirect('success')

            else:
                return Response({
                    "alert": f"Account not found, please try again."
                }, status=status.HTTP_404_NOT_FOUND)
