import random
import string
from django.db import models



def generate_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


class User(models.Model):
    phone_number = models.CharField(max_length=12)
    invite_code = models.CharField(max_length=6, default=generate_invite_code, unique=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone_number)


class Referral(models.Model):
    user = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred_users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_user} referred by {self.user}"
