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
        # If birthday hasn't occurred yet this year
        if birthday > today:
            return today.year - dob.year - 1
        else:
            return today.year - dob.year
    except AttributeError:
        return ''

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})