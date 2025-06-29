import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date

def generate_username(full_name):
    base_username = slugify(full_name, allow_unicode=True)
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{base_username}{random_suffix}"
        if not User.objects.filter(username=username).exists():
            return username


class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_via_message(self):
        pass
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(body=f'your otp is:{self.otp}', from_=f'{settings.TWILIO_PHONE_NUMBER}',
        #                        to=f'{settings.TWILIO_COUNTRY_CODE}{self.phone_number}')


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def generate_random_password():
    return str(random.randint(100000, 999999))  # 6-digit password


def str_to_bool(s):
    return s.lower() in ['true', '1', 'yes', 'y', 'True']