import redis
import random
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def redis_set_otp(phone_number):
    redis_instance = redis.Redis(host='localhost', port=6379, db=0)
    code = random.randint(1111, 9999)
    redis_instance.set(phone_number, code)
    redis_instance.expire(phone_number, 180)
    redis_instance.close()
    return code


def redis_check_otp(phone_number, otp_code):
    redis_instance = redis.Redis(host='localhost', port=6379, db=0)
    otp = redis_instance.get(phone_number)
    redis_instance.close()

    if otp:
        if int(otp) == otp_code:
            return otp
        raise ValidationError(_('OTP code incorrect!'))
    raise ValidationError(_('OTP code expired!'))
