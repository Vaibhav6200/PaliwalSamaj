from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class QualificationDetailInline(admin.StackedInline):
    model = QualificationDetail
    extra = 0

class OccupationDetailInline(admin.StackedInline):
    model = OccupationDetail
    extra = 0


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'family_code',
        'family_head',
        'paitrik_address',
        'paitrik_address_village',
        'paitrik_address_city',
        'paitrik_address_state',
        'paitrik_address_pincode',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'name')
    list_filter = ('name', 'family_head', 'family_code')


class CustomUserAdmin(DefaultUserAdmin):
    search_fields = ('username',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    inlines = [QualificationDetailInline, OccupationDetailInline]

    list_display = (
        'id',
        'user',
        'family',
        'full_name',
        'email',
        'father_name',
        'mother_name',
        'date_of_birth',
        'birth_place',
        'birth_time',
        'gender',
        'marital_status',
        'height',
        'phone_number',
        'whatsapp_number',
        'gotra',
        'current_address',
        'current_address_village',
        'current_address_city',
        'current_address_state',
        'current_address_pincode',
        'profile_image',
        'qualification_type',
        'occupation_type',
        'facebook_link',
        'instagram_link',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'family', 'user')
    list_filter = ('full_name', 'family', 'phone_number')


@admin.register(QualificationDetail)
class QualificationDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'school_class',
        'school_name',
        'college_name',
        'degree_name',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'member')
    list_filter = ('member',)


@admin.register(OccupationDetail)
class OccupationDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'company_name',
        'company_location',
        'job_description',
        'business_name',
        'business_location',
        'business_description',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'member')
    list_filter = ('member',)


@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'subtitle',
        'image',
        'content',
        'category',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'title')
    list_filter = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'parent',
        'sender',
        'content',
        'created_at'
    )
    list_display_links = ('id', 'post', 'sender')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'created_at',
    )
    list_display_links = ('id', 'email')
    list_filter = ('email',)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'message',
        'created_at',
    )
    list_display_links = ('id', 'name')
    list_filter = ('name','email')


@admin.register(Sandesh)
class SandeshAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'message',
        'image',
        'created_at',
    )
    list_display_links = ('id', 'sender')
    list_filter = ('sender', 'receiver')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'year',
        'media_type',
        'image',
        'video',
        'created_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('year',)


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'created_at',
    )
    list_display_links = ('id', 'title')


@admin.register(DisplayMemberGroup)
class DisplayMemberGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group_name',
        'group_rank',
        'created_at',
    )
    list_display_links = ('id', 'group_name')


@admin.register(DisplayMember)
class DisplayMemberAdmin(admin.ModelAdmin):
    def member_image_thumbnail(self, object):
        if object.member_image:
            return format_html(
                '<img src="{}" width="50px"  height="50px" style="border-radius: 50%; " />'.format(object.member_image.url))
        else:
            return format_html('<img src="/static/images/user-icon.png" width="50" height="50" style="border-radius: 50%;" />')

    list_display = (
        'member_image_thumbnail',
        'member_name',
        'group',
        'rank',
        'role',
        'location',
        'phone_number',
        'created_at',
    )
    list_display_links = ('member_name',)
    member_image_thumbnail.short_description = "member photo"
    list_filter = ('group',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'state_name',
        'created_at',
    )
    list_display_links = ('id', 'state_name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'city_name',
        'state',
        'created_at',
    )
    list_display_links = ('id', 'city_name')


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'village_name',
        'city',
        'created_at',
    )
    list_display_links = ('id', 'village_name')