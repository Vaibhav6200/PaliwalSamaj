from celery import shared_task
from .models import Member, QualificationDetail, OccupationDetail
from google.transliteration import transliterate_text
from indicate import transliterate


@shared_task
def translate_member_fields(member_id, lang='en'):
    member = Member.objects.get(id=member_id)
    qualification_instance = QualificationDetail.objects.get(member=member)
    occupation_instance = OccupationDetail.objects.get(member=member)

    def detect_and_assign(obj, modal_field):
        try:
            if lang == 'en':
                value = getattr(obj, modal_field)
                if not value:
                    return
                transliterated = transliterate_text(value, lang_code='hi')
                setattr(obj, f"{modal_field}_en", value)
                setattr(obj, f"{modal_field}_hi", transliterated)
            elif lang == 'hi':
                value = getattr(obj, f"{modal_field}_hi")
                if not value:
                    return
                setattr(obj, f"{modal_field}_hi", value)
                # transliterated = transliterate_text(value, lang_code='en')
                transliterated = transliterate.hindi2english(value)
                setattr(obj, f"{modal_field}_en", transliterated)

        except Exception as e:
            print(f"Translation failed for field '{modal_field}': {e}")

    member_modal_translation_fields = ['first_name', 'last_name', 'father_name', 'mother_name', 'birth_place', 'current_address', 'current_address_village', 'current_address_city', 'current_address_state']
    qualification_modal_translation_fields = ['school_name', 'college_name']
    occupation_modal_translation_fields = ['company_name', 'company_location', 'job_description', 'business_name', 'business_location', 'business_description']

    for field in member_modal_translation_fields:
        detect_and_assign(member, field)
    member.save()

    for field in qualification_modal_translation_fields:
        detect_and_assign(qualification_instance, field)
    qualification_instance.save()

    for field in occupation_modal_translation_fields:
        detect_and_assign(occupation_instance, field)
    occupation_instance.save()
