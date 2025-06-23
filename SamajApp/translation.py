from modeltranslation.translator import translator, TranslationOptions
from .models import Member, QualificationDetail, OccupationDetail, Culture


class MemberTranslationOptions(TranslationOptions):
    fields = (
        'full_name',
        'father_name',
        'mother_name',
        'birth_place',
        'current_address',
        'current_address_village',
        'current_address_city',
        'current_address_state',
    )

class QualificationTranslationOptions(TranslationOptions):
    fields = (
        'school_name',
        'college_name',
    )

class OccupationTranslationOptions(TranslationOptions):
    fields = (
        'company_name',
        'company_location',
        'job_description',
        'business_name',
        'business_location',
        'business_description',
    )

class CultureTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )

translator.register(Member, MemberTranslationOptions)
translator.register(QualificationDetail, QualificationTranslationOptions)
translator.register(OccupationDetail, OccupationTranslationOptions)
translator.register(Culture, CultureTranslationOptions)
