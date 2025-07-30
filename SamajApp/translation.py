from modeltranslation.translator import translator, TranslationOptions
from .models import Member, QualificationDetail, OccupationDetail, Culture, DisplayMemberGroup, DisplayMember, State, \
    City, Village


class MemberTranslationOptions(TranslationOptions):
    fields = (
        'full_name',
        'father_name',
        'mother_name',
        'birth_place',
        'current_address',
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

class DisplayMemberGroupTranslationOptions(TranslationOptions):
    fields = (
        'group_name',
    )

class DisplayMemberTranslationOptions(TranslationOptions):
    fields = (
        'member_name',
        'location',
    )

class StateTranslationOptions(TranslationOptions):
    fields = (
        'state_name',
    )

class CityTranslationOptions(TranslationOptions):
    fields = (
        'city_name',
    )

class VillageTranslationOptions(TranslationOptions):
    fields = (
        'village_name',
    )

translator.register(State, StateTranslationOptions)
translator.register(City, CityTranslationOptions)
translator.register(Village, VillageTranslationOptions)
translator.register(Member, MemberTranslationOptions)
translator.register(QualificationDetail, QualificationTranslationOptions)
translator.register(OccupationDetail, OccupationTranslationOptions)
translator.register(Culture, CultureTranslationOptions)
translator.register(DisplayMemberGroup, DisplayMemberGroupTranslationOptions)
translator.register(DisplayMember, DisplayMemberTranslationOptions)
