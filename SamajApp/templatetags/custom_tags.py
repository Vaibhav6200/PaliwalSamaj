from django import template
from datetime import date


register = template.Library()


@register.filter(name='get_member_age')
def get_member_age(dob):
    if not dob:
        return ''
    today = date.today()
    try:
        birthday = dob.replace(year=today.year)
    except ValueError:
        # Handles leap year issue (Feb 29 in non-leap years → fallback to Feb 28)
        birthday = date(today.year, 2, 28)
        # If birthday hasn't occurred yet this year
    if birthday > today:
        return today.year - dob.year - 1
    return today.year - dob.year


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})