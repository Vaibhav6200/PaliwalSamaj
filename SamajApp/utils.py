import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User


def generate_username(first_name, last_name):
    base_username = slugify(f"{first_name}.{last_name}")
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{base_username}{random_suffix}"
        if not User.objects.filter(username=username).exists():
            return username