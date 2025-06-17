from django.contrib import admin
from .models import *


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'family_code', 'family_head', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'family',
        'first_name',
        'last_name',
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


@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'subtitle',
        'slug',
        'image',
        'content',
        'category',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'title')


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


@admin.register(SamajMemberRoles)
class SamajMemberRolesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member_name',
        'member_image',
        'role',
        'location',
        'phone_number',
        'created_at',
    )
    list_display_links = ('id', 'member_name')


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


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'created_at',
    )
    list_display_links = ('id', 'title')


