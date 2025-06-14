import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def generate_username(first_name, last_name):
    base_username = slugify(f"{first_name}.{last_name}")
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{base_username}{random_suffix}"
        if not User.objects.filter(username=username).exists():
            return username