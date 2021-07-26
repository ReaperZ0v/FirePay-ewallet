from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views 

urlpatterns = [
    path("sign-up/", views.RegisterAPIView.as_view(), name="register"),
    path("verify/", views.VerifyAPIView.as_view(), name="verify"),
    path('login/', views.TokenObtainPairView.as_view(), name="token_obtain_view")
]