import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
import logging
from paliwalsamaj import settings
from .models import State, City, Village, SponsorAd
from django.utils import translation
from google.transliteration import transliterate_text
from indicate import transliterate


logger = logging.getLogger(__name__)


def show_ad(request):
    now = datetime.now()
    last_seen_str = request.session.get("ad_last_seen")     # 25-08-09 01:03:14
    show_ad_now = False

    logger.debug("NOW: %s", now)
    logger.debug("LAST SEEN STR: %s", last_seen_str)
    logger.debug("SESSION KEYS: %s", list(request.session.keys()))

    if last_seen_str:
        last_seen = datetime.strptime(last_seen_str, "%Y-%m-%d %H:%M:%S")
        logger.debug("last_seen: %s", last_seen)
        logger.debug("now - last_seen: %s", now - last_seen)

        if now - last_seen >= timedelta(minutes = settings.SPONSOR_REPEAT_MINUTES):
            show_ad_now = True
    else:
        show_ad_now = True

    if show_ad_now:
        request.session["show_ad"] = True
        request.session["ad_last_seen"] = now.strftime("%Y-%m-%d %H:%M:%S")

        # Load active sponsor ad
        active_ad = SponsorAd.objects.filter(is_active=True).first()

        if active_ad:
            request.session["sponsor_timer"] = f"{int(settings.SPONSOR_TIMER) * 1000}"
            request.session["sponsor_name"] = active_ad.name
            request.session["sponsor_message"] = active_ad.message
            request.session["sponsor_image_url"] = active_ad.image.url
    else:
        request.session["show_ad"] = False

    logger.debug("show_ad: %s", request.session["show_ad"])
    logger.debug("ad_last_seen: %s", request.session["ad_last_seen"])


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