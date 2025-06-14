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

