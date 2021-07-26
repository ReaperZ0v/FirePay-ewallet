from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework import serializers
from . import models 
import random 


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ("first_name", "last_name", "email", "tax_id", "username", "phone_number", "password")
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        profile = models.Profile.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            username = validated_data["username"],
            phone_number = validated_data["phone_number"],
            email = validated_data["email"],
            tax_id = validated_data["tax_id"],
        )

        profile.set_password(validated_data["password"])
        profile.save()

        return profile 


class VerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=60)


