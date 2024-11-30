from rest_framework import serializers
from .models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'invite_code', 'referred_by']


class ReferralSerializer(serializers.ModelSerializer):
    referred_user = UserSerializer()

    class Meta:
        model = Referral
        fields = ['referred_user', 'created_at']