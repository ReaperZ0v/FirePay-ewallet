from django.urls import path 
from . import views 

urlpatterns = [
    path("my-wallet/", views.AccountWalletView.as_view(), name="wallet"),
    path("transactions/", views.TransactionsListView.as_view(), name="transactions"),
    path("pay/", views.MakePaymentView.as_view(), name="pay"),
    path("transfer-success/", views.SuccessView.as_view(), name="success")
]