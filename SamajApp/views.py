import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from SamajApp.models import NewsEvent, Comment, Member, Family, Newsletter, QualificationDetail, OccupationDetail, \
    Suggestion
from django.contrib import messages
from .utils import generate_username, MessageHandler
from datetime import date, timedelta


def site_login(request):
    return render(request, 'Samaj/login.html')


def index(request):
    news_events_obj = NewsEvent.objects.all()
    context = {
        'news_and_events': news_events_obj,
    }
    return render(request, 'Samaj/index.html', context)


@login_required
def bio_data(request):
    context = {'family_code': Member.objects.get(user=request.user).family.family_code}
    if request.method == 'POST':
        edit_member_user_id = request.POST.get('user_id')
        context['edit_member'] = Member.objects.get(user__id = edit_member_user_id)
    return render(request, 'Samaj/bio_data.html', context)


@login_required
def handle_bio_data_form(request, family_code):
    if request.method == 'POST':
        user_id = request.POST.get('edit_member_user_id')
        family = get_object_or_404(Family, family_code=family_code)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Check if we're updating or creating
        if user_id:
            # UPDATE FLOW
            user = get_object_or_404(User, id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            member, _ = Member.objects.get_or_create(user=user, family=family)
            messages.success(request, 'Profile Updated Successfully')
        else:
            # CREATE FLOW
            user = User.objects.create(
                username=generate_username(first_name, last_name),
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            member = Member(user=user, family=family)
            messages.success(request, 'Member Added Successfully')

        # Common fields (both for create & update)
        member.father_name = request.POST.get('father_name')
        member.mother_name = request.POST.get('mother_name')
        member.date_of_birth = request.POST.get('date_of_birth')
        member.birth_place = request.POST.get('birth_place')
        member.birth_time = request.POST.get('birth_time')
        member.gender = request.POST.get('gender')
        member.marital_status = request.POST.get('marital_status')
        member.height = request.POST.get('height')
        member.phone_number = request.POST.get('phone_number')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.gotra = request.POST.get('gotra')
        member.current_address = request.POST.get('address')
        member.qualification_type = request.POST.get('qualification')
        member.occupation_type = request.POST.get('occupation')
        member.instagram_link = request.POST.get('instagram_link')
        member.facebook_link = request.POST.get('facebook_link')

        profile_image = request.FILES.get('profileImage')
        if profile_image:
            member.profile_image = profile_image

        member.save()

        # Qualification Details
        qualification, _ = QualificationDetail.objects.get_or_create(member=member)
        qualification.school_class = request.POST.get('school_class')
        qualification.school_name = request.POST.get('school_name')
        qualification.college_name = request.POST.get('college_name')
        qualification.degree_name = request.POST.get('degree_name')
        qualification.save()

        # Occupation Details
        occupation, _ = OccupationDetail.objects.get_or_create(member=member)
        occupation.company_name = request.POST.get('company_name')
        occupation.company_location = request.POST.get('job_location')
        occupation.job_description = request.POST.get('job_description')
        occupation.business_name = request.POST.get('business_name')
        occupation.business_location = request.POST.get('business_location')
        occupation.business_description = request.POST.get('business_description')
        occupation.save()
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


def community(request):
    context = {
        'min_age_default_value': 10,
        'max_age_default_value': 20,
    }

    community_members = Member.objects.all()
    if request.method == 'GET':
        name = request.GET.get('name')
        min_age_value = request.GET.get('min_age_value')
        max_age_value = request.GET.get('max_age_value')
        gotra = request.GET.get('gotra')
        gender = request.GET.get('gender')
        education = request.GET.get('education')

        # 🔍 Name filtering (splitting and checking each word in both first_name and last_name)
        if name:
            name_parts = name.strip().split()
            for part in name_parts:
                community_members = (
                    community_members.filter(user__first_name__icontains=part) |
                    community_members.filter(user__last_name__icontains=part)
                )

        today = date.today()
        if min_age_value and max_age_value:
            context['min_age_default_value'] = min_age_value
            context['max_age_default_value'] = max_age_value

            max_dob = today - timedelta(days=int(min_age_value) * 365)
            min_dob = today - timedelta(days=int(max_age_value) * 365)
            community_members = community_members.filter(date_of_birth__range=(min_dob, max_dob))
        elif min_age_value:
            context['min_age_default_value'] = min_age_value
            max_dob = today - timedelta(days=int(min_age_value) * 365)
            community_members = community_members.filter(date_of_birth__lte=max_dob)
        elif max_age_value:
            context['max_age_default_value'] = max_age_value
            min_dob = today - timedelta(days=int(max_age_value) * 365)
            community_members = community_members.filter(date_of_birth__gte=min_dob)

        if gotra:
            community_members = community_members.filter(gotra__icontains=gotra)

        if gender:
            community_members = community_members.filter(gender=gender)

        if education:
            community_members = community_members.filter(qualification_detail__degree_name__icontains=education)

    context['community_members'] = community_members
    return render(request, 'Samaj/community.html', context)


@login_required
def my_family(request):
    login_member = Member.objects.get(user = request.user)
    all_family_members = Member.objects.filter(family=login_member.family)

    context = {
        'all_family_members': all_family_members,
        'family_head': login_member.family.family_head,
    }
    return render(request, 'Samaj/my_family.html', context)


def news_and_events(request):
    news_events_obj = NewsEvent.objects.all().order_by('-created_at')
    context = {
        'news_and_events': news_events_obj,
    }
    return render(request, 'Samaj/news_and_events.html', context)


def news_events_detail(request, event_slug):
    post = NewsEvent.objects.get(slug=event_slug)
    comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # For reply handling
        parent = Comment.objects.get(id=parent_id) if parent_id else None

        Comment.objects.create(
            post = post,
            sender = Member.objects.get(user=request.user),
            content = content,
            parent=parent
        )
        messages.success(request, 'Comment Posted Successfully')
        return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

    recent_posts = NewsEvent.objects.exclude(id=post.id).order_by('-created_at')[:3]

    context = {
        'post': post,
        'recent_posts': recent_posts,
        'comments': comments
    }
    return render(request, 'Samaj/news_events_detail.html', context)


def paliwal_samaj_history(request):
    return render(request, "Culture/P1_paliwal_samaj_history.html")


def karyarat_sangathan(request):
    return render(request, "Culture/P2_karyarat_sangathan.html")


def sandhya_vandana(request):
    return render(request, "Culture/P3_sandhya_vandana.html")


def brahman_16_sanskar(request):
    return render(request, "Culture/P4_brahman_16_sanskar.html")


def upanayan_sanskar(request):
    return render(request, "Culture/P5_upanayan_sanskar.html")


def mewar_paliwal_samaj_ke_teerth_purohit(request):
    return render(request, "Culture/P6_mewar_paliwal_samaj_ke_teerth_purohit.html")


def vivah_karyakram(request):
    return render(request, "Culture/P7_vivah_karyakram.html")


def vivah_geet(request):
    return render(request, "Culture/P8_vivah_geet.html")


def antyeshti_kriya_paddhati(request):
    return render(request, "Culture/P9_antyeshti_kriya_paddhati.html")


def dasva_gyarahva_evam_barahva_karyakram(request):
    return render(request, "Culture/P10_dasva_gyarahva_evam_barahva_karyakram.html")


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, 'This email is already subscribed to the newsletter.')
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, 'You have successfully subscribed to the newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


def suggestions(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and message and email:
            Suggestion.objects.create(name = name, email = email, message = message)
            messages.success(request, 'Thank you! Your suggestion has been submitted.')
        else:
            messages.error(request, 'All fields are required. Please complete the form.')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


@login_required
def phone_number_send_otp(request):
    if request.method == 'POST':
        contact_input = request.POST.get('contact_input', None)

        if not contact_input:
            messages.error(request, 'Please enter a phone number.')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        # Check if the number exists in either phone_number or whatsapp_number
        member = (
            Member.objects.filter(phone_number=contact_input).first() or
            Member.objects.filter(whatsapp_number=contact_input).first()
        )

        if member:
            verification_code = random.randint(100000, 999999)
            handler = MessageHandler(phone_number=contact_input, otp=verification_code)
            handler.send_otp_via_message()
            request.session['phone_verification_code'] = verification_code
            messages.success(request, f'OTP send to your registered number: {contact_input}')
        else:
            messages.error(request,'This number is not registered.')

        context = {
            'phone_otp': True
        }
        return render(request, 'Profile/otp_verification.html', context)
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

