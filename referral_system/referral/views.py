from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Referral
from .serializers import UserSerializer


class PhoneNumberLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Simulate sending an OTP (for demo, we just log it)
        otp = '1234'
        print(f"OTP for {phone_number}: {otp}")

        # Save the phone number temporarily (you can use a cache for production)
        request.session['phone_number'] = phone_number
        request.session['otp'] = otp

        return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)


class OTPVerificationView(APIView):
    def post(self, request):
        phone_number = request.session.get('phone_number')
        otp = request.data.get('otp')

        if otp != request.session.get('otp'):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)
        return Response({'user_id': user.id, 'created': created}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        referrals = Referral.objects.filter(user=user)
        referred_users = [ref.referred_user.phone_number for ref in referrals]

        return Response({
            'id': user.id,
            'phone_number': user.phone_number,
            'invite_code': user.invite_code,
            'referred_by': user.referred_by.invite_code if user.referred_by else None,
            'referred_users': referred_users,
        })

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        invite_code = request.data.get('invite_code')

        if user.referred_by:
            return Response({'error': 'Referral code already used'}, status=status.HTTP_400_BAD_REQUEST)

        referred_by = User.objects.filter(invite_code=invite_code).first()
        if not referred_by:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_404_NOT_FOUND)

        user.referred_by = referred_by
        user.save()

        Referral.objects.create(user=referred_by, referred_user=user)
        return Response({'message': 'Referral code activated'}, status=status.HTTP_200_OK)
