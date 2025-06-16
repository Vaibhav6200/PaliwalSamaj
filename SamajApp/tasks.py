from celery import shared_task
from django.conf import settings
from google.cloud import translate_v2 as translate
from .models import Member, QualificationDetail, OccupationDetail
import time
from django.utils import translation
from google.transliteration import transliterate_text


client = translate.Client.from_service_account_json(settings.GCP_KEY_PATH)


@shared_task
def translate_member_fields(member_id):
    member = Member.objects.get(id=member_id)
    qualification_instance = QualificationDetail.objects.get(member=member)
    occupation_instance = OccupationDetail.objects.get(member=member)

    def detect_and_assign(obj, modal_field):
        value = getattr(obj, modal_field)
        print(f"value: {value}")
        if not value:
            return

        try:
            current_language = translation.get_language()
            if current_language == 'en':
                transliterated = transliterate_text(value, lang_code='hi')
                setattr(obj, f"{modal_field}_en", value)
                setattr(obj, f"{modal_field}_hi", transliterated)
                print(f"Transliterated Hindi: {transliterated}")
            else:
                transliterated = transliterate_text(value, lang_code='en')
                setattr(obj, f"{modal_field}_hi", value)
                setattr(obj, f"{modal_field}_en", transliterated)


            # if current_language == 'hi':
            #     setattr(obj, f"{modal_field}_hi", value)
            #
            #     translated = client.translate(value, target_language='en', format_='text')['translatedText']
            #     setattr(obj, f"{modal_field}_en", translated)
            #
            #     print(f"User input Hindi: {value}")
            # else:
            #     setattr(obj, f"{modal_field}_en", value)
            #     translated = client.translate(value, target_language='hi', format_='text')['translatedText']
            #     setattr(obj, f"{modal_field}_hi", translated)
            #     print(f"Translated Hindi: {translated}")

        except Exception as e:
            print(f"Translation failed for field '{modal_field}': {e}")
        time.sleep(1)

    member_modal_translation_fields = ['first_name', 'last_name', 'father_name', 'mother_name', 'birth_place', 'current_address', 'current_address_city', 'current_address_state']
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
