import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date
from .models import State, City, Village
from django.utils import translation
from google.transliteration import transliterate_text
from indicate import transliterate
from modeltranslation.utils import build_localized_fieldname


def get_or_create_address(state_name, city_name, village_name):
    current_language = translation.get_language()
    if current_language == 'en':
        state_name_hi = transliterate_text(state_name, lang_code='hi')
        city_name_hi = transliterate_text(city_name, lang_code='hi')
        village_name_hi = transliterate_text(village_name, lang_code='hi')

        state, _ = State.objects.get_or_create(state_name=state_name.strip().lower(), state_name_hi=state_name_hi)
        city, _ = City.objects.get_or_create(city_name=city_name.strip().lower(), city_name_hi=city_name_hi, state=state)
        village, _ = Village.objects.get_or_create(village_name=village_name, village_name_hi=village_name_hi, city=city)
    elif current_language == 'hi':
        state_name_en = transliterate.hindi2english(state_name)
        city_name_en = transliterate.hindi2english(city_name)
        village_name_en = transliterate.hindi2english(village_name)

        # NOTE: django-modeltranslation stores the default language (usually 'en') in the base field (state_name), and other languages like Hindi go into state_name_hi, city_name_hi, etc.
        state, _ = State.objects.get_or_create(state_name=state_name, state_name_en=state_name_en)
        city, _ = City.objects.get_or_create(city_name=city_name, city_name_en=city_name_en, state=state)
        village, _ = Village.objects.get_or_create(village_name=village_name, village_name_en=village_name_en, city=city)
    else:
        raise ValueError(f"Unsupported language: {current_language}")   # Handle unexpected languages
    return state, city, village


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