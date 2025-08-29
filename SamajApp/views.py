import random
import string
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch, Case, When, Value, IntegerField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from SamajApp.models import NewsEvent, Comment, Member, Family, Newsletter, QualificationDetail, OccupationDetail, \
    Suggestion, DisplayMember, Sandesh, Gallery, Culture, DisplayMemberGroup, Village, City, State, SponsorAd, SMSLog, \
    Support, Degree
from django.contrib import messages
from paliwalsamaj import settings
from .forms import CultureCreatePostForm
from .utils import generate_username, calculate_age, get_or_create_address, show_ad, build_market_buzzer_sms_payload
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator
from .tasks import translate_member_fields
from django.utils import translation
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
import logging
from django.db.models.functions import Lower


logger = logging.getLogger(__name__)


def site_login(request):
    show_ad(request)
    if request.method == 'POST':
        phone = request.POST.get('contact_input')
        password = request.POST.get('password')

        member = Member.objects.filter(phone_number=phone)
        if not member.exists():
            messages.error(request, 'No Member Found with this Phone Number.')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        member = member.first()
        user = authenticate(request, username=member.user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Login Successful, Welcome {member.full_name}.')
            return redirect('samaj:index')
        else:
            messages.error(request, 'Invalid password.')

    return render(request, 'Samaj/login.html')


@csrf_exempt
def reset_member_password(request):
    if request.method == 'POST':
        phone = request.POST.get('contact_input')

        member = Member.objects.filter(phone_number=phone)
        if not member.exists():
            messages.error(request, "No member found with this number.")
            return redirect(request.META.get('HTTP_REFERER', 'samaj:site_login'))

        if not settings.ENABLE_SMS:
            messages.error(request, "Our SMS Service is currently disabled.")
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        member = member.first()

        # Generate random 6-digit password
        new_password = ''.join(random.choices(string.digits, k=6))

        # Reset password
        user = member.user
        user.set_password(new_password)
        user.save()

        reference_id = random.randint(10000, 99999)
        full_name = 'User'
        if member.full_name_en:
            full_name = member.full_name_en

        market_buzzer_xml_payload = build_market_buzzer_sms_payload(full_name, new_password, phone, reference_id)
        market_buzzer_sms_header = {"Content-Type": "application/xml"}
        response = requests.post(settings.BUZZER_SMS_URL, data=market_buzzer_xml_payload.encode("utf-8"), headers=market_buzzer_sms_header)

        # FAST2SMS Send via SMS
        # fast2sms_payload = {
        #     'sender_id': settings.FAST2SMS_SENDER_ID,
        #     'message': settings.FAST2SMS_MESSAGE_ID,
        #     'variables_values': f"{member.full_name_en}|{new_password}",
        #     'route': settings.FAST2SMS_ROUTE,
        #     'numbers': phone
        # }
        # fast2sms_headers = {
        #     'authorization': settings.FAST2SMS_API_KEY,
        #     'Content-Type': 'application/x-www-form-urlencoded'
        # }
        # response = requests.post(settings.FAST2SMS_URL, data=fast2sms_payload, headers=fast2sms_headers)

        if response.status_code == 200:
            messages.success(request, "New password sent via SMS.")
        else:
            messages.error(request, "Failed to send SMS. Please try again.")

        # Saving SMS log regardless of success/failure
        SMSLog.objects.create(
            member=member,
            phone_number=phone,
            message=f"Dear {full_name}, your login password for Shree Bada Paliwal Samaj website is {new_password}.",
            reference_id=reference_id,
            status_code=response.status_code,
            response_text=response.text
        )
        return render(request, 'Samaj/login.html', {'phone_number': phone})
    return redirect('samaj:site_login')


def site_logout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('samaj:index')


def index(request):
    show_ad(request)
    news_events_obj = NewsEvent.objects.all()

    # Get all groups and prefetch members ordered by rank
    display_groups = DisplayMemberGroup.objects.order_by('group_rank').prefetch_related(
        Prefetch(
            'displaymember_set',
            queryset=DisplayMember.objects.order_by('rank')
        )
    )

    context = {
        'news_and_events': news_events_obj,
        'display_groups': display_groups,
    }
    return render(request, 'Samaj/index.html', context)


@login_required
def bio_data(request):
    show_ad(request)
    context = {
        'family_code': Member.objects.get(user=request.user).family.family_code,
        'gotras': Member.GOTRA_CHOICES,
        'degrees': Degree.objects.all().order_by('degree_name'),
        'qualification_type': Member.QUALIFICATION_CHOICES,
        'occupation_type': Member.OCCUPATION_CHOICES,
    }
    if request.method == 'POST':
        edit_member_user_id = request.POST.get('user_id')
        context['edit_member'] = Member.objects.get(user__id = edit_member_user_id)
    return render(request, 'Samaj/bio_data.html', context)


@login_required
def handle_bio_data_form(request, family_code):
    if request.method == 'POST':

        user_id = request.POST.get('edit_member_user_id')
        family = get_object_or_404(Family, family_code=family_code)

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Check if we're updating or creating
        if user_id:
            # UPDATE FLOW
            user = get_object_or_404(User, id=user_id)
            member, _ = Member.objects.get_or_create(user=user, family=family)
            messages.success(request, 'Profile Updated Successfully')
        else:
            # CREATE FLOW
            user = User.objects.create(username=generate_username(full_name))
            member = Member(user=user, family=family)
            messages.success(request, 'Member Added Successfully')

        # Extracting Data from Form
        date_of_birth = request.POST.get('date_of_birth')
        birth_time = request.POST.get('birth_time')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        birth_place = request.POST.get('birth_place')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        height = request.POST.get('height')
        phone_number = request.POST.get('phone_number')
        whatsapp_number = request.POST.get('whatsapp_number')
        gotra = request.POST.get('gotra')
        qualification = request.POST.get('qualification')
        occupation = request.POST.get('occupation')
        instagram_link = request.POST.get('instagram_link')
        facebook_link = request.POST.get('facebook_link')
        profile_image = request.FILES.get('profileImage')
        school_class = request.POST.get('school_class')
        school_name = request.POST.get('school_name')
        college_name = request.POST.get('college_name')
        degree_code = request.POST.get('degree_name')
        company_name = request.POST.get('company_name')
        job_location = request.POST.get('job_location')
        job_description = request.POST.get('job_description')
        business_name = request.POST.get('business_name')
        business_location = request.POST.get('business_location')
        business_description = request.POST.get('business_description')
        state = request.POST.get('state')
        city = request.POST.get('city')
        village = request.POST.get('village')

        state, city, village = get_or_create_address(state, city, village)

        member.full_name = full_name
        if email:
            member.email = email
        if father_name:
            member.father_name = father_name
        if mother_name:
            member.mother_name = mother_name
        if birth_place:
            member.birth_place = birth_place
        if date_of_birth:
            member.date_of_birth = date_of_birth
        if birth_time:
            member.birth_time = birth_time
        if gender:
            member.gender = gender
        if marital_status:
            member.marital_status = marital_status
        if height:
            member.height = height
        if address:
            member.current_address = address
        if phone_number:
            member.phone_number = phone_number
        if whatsapp_number:
            member.whatsapp_number = whatsapp_number
        if gotra:
            member.gotra = gotra
        if qualification:
            member.qualification_type = qualification
        if occupation:
            member.occupation_type = occupation
        if instagram_link:
            member.instagram_link = instagram_link
        if facebook_link:
            member.facebook_link = facebook_link
        if state:
            member.current_address_state = state
        if city:
            member.current_address_city = city
        if village:
            member.current_address_village = village

        if profile_image:
            # Delete previous image file if exists
            if member.profile_image and default_storage.exists(member.profile_image.name):
                member.profile_image.delete(save=False)
            member.profile_image = profile_image
        member.save()

        # Qualification Details
        if not member.qualification_type == 'none':
            qualification, _ = QualificationDetail.objects.get_or_create(member=member)
            if member.qualification_type == 'school':
                qualification.school_class = int(school_class) if school_class else None
                qualification.school_name = school_name
                qualification.college_name = None
            else:
                qualification.school_class = None
                qualification.school_name = None
                qualification.college_name = college_name
                if Degree.objects.filter(degree_code=degree_code).exists():
                    qualification.degree = Degree.objects.get(degree_code=degree_code)
            qualification.save()

        # Occupation Details
        occupation, _ = OccupationDetail.objects.get_or_create(member=member)
        if member.occupation_type == 'job':
            occupation.company_name = company_name
            occupation.company_location = job_location
            occupation.job_description = job_description

            # Clear business fields
            occupation.business_name = None
            occupation.business_location = None
            occupation.business_description = None

        elif member.occupation_type == 'business':
            occupation.business_name = business_name
            occupation.business_location = business_location
            occupation.business_description = business_description

            # Clear Job fields
            occupation.company_name = None
            occupation.company_location = None
            occupation.job_description = None
        else:
            occupation.business_name = None
            occupation.business_location = None
            occupation.business_description = None
            occupation.company_name = None
            occupation.company_location = None
            occupation.job_description = None
        occupation.save()

        # submit task to celery for translations
        if settings.ENABLE_TRANSLITERATION:
            current_language = translation.get_language()
            try:
                translate_member_fields.delay(member.id, current_language)
            except Exception as e:
                logger.error(f"Celery task failed. Reason: {e}, So Translating Synchronously")
                translate_member_fields(member.id, current_language)
    return redirect('samaj:my_family')


@login_required
def handle_member_delete(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        delete_member_qs = Member.objects.filter(id=member_id)

        if not delete_member_qs.exists():
            messages.error(request, f'member does not exists')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        delete_member = delete_member_qs.first()
        login_member = Member.objects.filter(user=request.user).first()
        login_user_family = login_member.family

        # Check if the member to be deleted belongs to the same family
        if delete_member.family != login_user_family:
            messages.error(request, 'You can delete members of your own family only.')
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        # Check if the member to delete is the head of the family
        is_family_head = (login_user_family.family_head == delete_member)

        delete_member_name = f"{delete_member.full_name}"
        delete_member.delete()

        # If the deleted member was the family head, assign the logged-in user as the new family head
        if is_family_head:
            login_user_family.family_head = login_member
            login_user_family.save()
        messages.success(request, f'member {delete_member_name} removed from family')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


def community(request):
    show_ad(request)
    context = {
        'min_age_default_value': 1,
        'max_age_default_value': 100,
        'gotras': Member.GOTRA_CHOICES,
        'degrees': Degree.objects.all().order_by('degree_name'),
    }

    # Default: show all
    villages = Village.objects.all()
    cities = City.objects.all()
    states = State.objects.all()

    community_members = Member.objects.all()
    if request.method == 'GET':
        name = request.GET.get('full_name')
        min_age_value = request.GET.get('min_age_value')
        max_age_value = request.GET.get('max_age_value')
        gotra = request.GET.get('gotra')
        gender = request.GET.get('member_gender')
        education = request.GET.get('education')
        state = request.GET.get('state')
        city = request.GET.get('city')
        village = request.GET.get('village')
        phone_number = request.GET.get('phone_number')
        marital_status = request.GET.get('marital_status')


        # 🔍 Name filtering (splitting and checking each word in full_name)
        if name:
            context['name_filter_value'] = name
            name_parts = name.strip().split()

            for part in name_parts:
                community_members = (community_members.filter(full_name_en__icontains=part))

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
            context['gotra_filter_value'] = gotra
            community_members = community_members.filter(gotra__icontains=gotra)

        if gender:
            context['gender_filter_value'] = gender
            community_members = community_members.filter(gender=gender)

        if education:
            context['education_filter_value'] = education
            community_members = community_members.filter(qualification_detail__degree__degree_code__icontains=education)

        if phone_number:
            context['phone_number_filter_value'] = phone_number.strip()
            community_members = community_members.filter(phone_number__contains=phone_number.strip())

        if marital_status:
            context['marital_status_filter_value'] = marital_status
            community_members = community_members.filter(marital_status=marital_status)


        if state:
            context['state_filter_value'] = state
            community_members = community_members.filter(Q(current_address_state__state_name__icontains=state) | Q(current_address__icontains=state))
            states = State.objects.all()
            cities = City.objects.filter(state__state_name=state)
            villages = Village.objects.filter(city__state__state_name=state)

            # Check if the selected city still belongs to the selected state
            if city and City.objects.filter(city_name=city, state__state_name=state).exists():
                context['city_filter_value'] = city
                community_members = community_members.filter(Q(current_address_city__city_name__icontains=city) | Q(current_address__icontains=city))
                villages = Village.objects.filter(city__city_name=city)

                # Check if village belongs to city
                if village and Village.objects.filter(village_name=village, city__city_name=city).exists():
                    context['village_filter_value'] = village
                    community_members = community_members.filter(Q(current_address_village__village_name__icontains=village) | Q(current_address__icontains=village))
                else:
                    context.pop('village_filter_value', None)
            else:
                context.pop('city_filter_value', None)
                context.pop('village_filter_value', None)

        elif city:
            context['city_filter_value'] = city
            community_members = community_members.filter(Q(current_address_city__city_name__icontains=city) | Q(current_address__icontains=city))
            cities = City.objects.all()
            villages = Village.objects.filter(city__city_name=city)

            # Try to derive state from city
            city_obj = City.objects.filter(city_name=city).first()
            if city_obj:
                state = city_obj.state.state_name
                context['state_filter_value'] = state
                states = State.objects.all()
                cities = City.objects.filter(state__state_name=state)

            if village and Village.objects.filter(village_name=village, city__city_name=city).exists():
                context['village_filter_value'] = village
                community_members = community_members.filter(Q(current_address_village__village_name__icontains=village) | Q(current_address__icontains=village))
            else:
                context.pop('village_filter_value', None)

        elif village:
            context['village_filter_value'] = village
            community_members = community_members.filter(Q(current_address_village__village_name__icontains=village) | Q(current_address__icontains=village))
            village_obj = Village.objects.filter(village_name=village).first()
            if village_obj:
                city = village_obj.city.city_name
                state = village_obj.city.state.state_name
                context['city_filter_value'] = city
                context['state_filter_value'] = state
                cities = City.objects.filter(state__state_name=state)
                villages = Village.objects.filter(city__city_name=city)

    context.update({
        'states': states.order_by('state_name'),
        'cities': cities.order_by('city_name'),
        'villages': villages.order_by('village_name'),
        'records_count': community_members.count(),
    })

    paginator = Paginator(
        community_members.order_by(Lower('full_name')),
        settings.COMMUNITY_MEMBERS_PER_PAGE
    )
    page_number = request.GET.get('page')
    context['community_members'] = paginator.get_page(page_number)

    return render(request, 'Samaj/community.html', context)


@login_required
def my_family(request):
    show_ad(request)
    login_member = Member.objects.filter(user = request.user).first()
    all_family_members = Member.objects.filter(family=login_member.family)

    context = {
        'all_family_members': all_family_members,
        'family_head': login_member.family.family_head,
        'track_family_views_flag': login_member.family.track_family_views_flag,
        'family_views': login_member.family.family_views,
    }
    return render(request, 'Samaj/my_family.html', context)


def member_family_tree(request, member_id):
    show_ad(request)
    community_member = Member.objects.get(id = member_id)
    family_members = Member.objects.filter(family=community_member.family)

    if community_member.family.track_family_views_flag:
        community_member.family.family_views += 1
        community_member.family.save(update_fields=["family_views"])

    context = {
        'family_head': community_member.family.family_head,
        'family_members': family_members,
    }
    return render(request, 'Samaj/member_family_tree.html', context)


@login_required
def sandesh(request):
    show_ad(request)
    current_member = Member.objects.get(user=request.user)

    if request.method == 'POST':
        receiver = get_object_or_404(Member, phone_number=request.POST.get('contact_input'))

        sandesh_obj = Sandesh(
            sender=current_member,
            receiver=receiver,
            message = request.POST.get('message'),
        )

        image_file = request.FILES.get('image')
        if image_file:
            sandesh_obj.image = image_file
        sandesh_obj.save()

        messages.success(request, "Sandesh Sent!")
        return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


    filter_type = request.GET.get('shandesh_filter', 'all')  # default to 'all'

    if filter_type == 'receive':
        my_sandesh = Sandesh.objects.filter(receiver=current_member)
    elif filter_type == 'sent':
        my_sandesh = Sandesh.objects.filter(sender=current_member)
    else:
        my_sandesh = Sandesh.objects.filter(Q(sender=current_member) | Q(receiver=current_member))
    my_sandesh = my_sandesh.order_by('-created_at')

    context = {
        'my_sandesh': my_sandesh,
        'selected_filter': filter_type,  # for retaining selected option
    }
    return render(request, "Samaj/sandesh.html", context)


@login_required
def user_profile(request, member_id):
    show_ad(request)
    member = Member.objects.get(id=member_id)

    # Increment only if tracking is enabled
    if member.track_member_views_flag:
        member.profile_views += 1
        member.save(update_fields=["profile_views"])

    context = {
        'profile': member,
        'user_age': calculate_age(member.date_of_birth),
    }
    return render(request, "Samaj/user_profile.html", context)


def news_and_events(request):
    show_ad(request)
    query = request.GET.get('q')
    news_events_obj = NewsEvent.objects.all().order_by('-created_at')

    if query:
        keywords = query.lower().strip().split()
        q_object = Q()
        for word in keywords:
            q_object |= Q(title__icontains=word)
            q_object |= Q(subtitle__icontains=word)
            q_object |= Q(content__icontains=word)
            q_object |= Q(category__icontains=word)

        news_events_obj = NewsEvent.objects.filter(q_object).order_by('-created_at')

    paginator = Paginator(news_events_obj, 10)   # Apply pagination (e.g., 6 items per page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'news_and_events': page_obj,
        'query': query,
    }
    return render(request, 'Samaj/news_and_events.html', context)


def news_events_detail(request, event_slug):
    show_ad(request)
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
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        if name and message and email and phone_number:
            Suggestion.objects.create(name = name, email = email, phone_number=phone_number, message = message)
            messages.success(request, 'Thank you! Your suggestion has been submitted.')
        else:
            messages.error(request, 'All fields are required. Please complete the form.')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


def get_member_search_list(request):
    search_query = request.GET.get('search')
    payload = []
    if search_query:
        words = search_query.strip().split()
        query = Q()
        for word in words:
            query |= Q(phone_number__icontains=word)
            query |= Q(full_name_en__icontains=word)

        objs = (
            Member.objects
            .filter(query)
            .annotate(
                priority=Case(
                    # Exact match → Highest Priority
                    When(full_name__iexact=search_query, then=Value(0)),
                    # Starts with → second highest
                    When(full_name__istartswith=search_query, then=Value(1)),
                    # Everything else → lower priority
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by('priority')
        )

        for obj in objs:
            payload.append({
                'member_name': obj.full_name,
                'member_phone': obj.phone_number,
            })

    return JsonResponse({
        "status": True,
        "payload": payload
    })


def image_and_video_gallery(request):
    show_ad(request)
    context = {
        'years': Gallery.objects.filter(media_type='photo').values_list('year', flat=True).distinct().order_by('-year'),
        'images': Gallery.objects.filter(media_type='photo'),
        'videos': Gallery.objects.filter(media_type='video'),
    }
    return render(request, 'Samaj/image_and_video_gallery.html', context)


def culture_details(request, culture_slug=None):
    show_ad(request)
    culture_obj = Culture.objects.get(slug=culture_slug)
    return render(request, "Samaj/culture_details.html", {'culture': culture_obj})


def culture_create_post(request):
    culture_obj = None

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'edit':
            culture_id = request.POST.get('culture_id')
            culture_obj = Culture.objects.filter(id = culture_id).first()

            if not culture_obj:
                messages.error(request, 'Culture Object Not Found')
                return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

            form = CultureCreatePostForm(request.POST, request.FILES, instance=culture_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Culture Updated Successfully')
                return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

        elif action == 'add':
            form = CultureCreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Created')
                return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
        else:
            form = CultureCreatePostForm()
    else:
        action = request.GET.get('action')
        culture_id = request.GET.get('culture_id')
        if action == 'edit' and culture_id:
            culture_obj = Culture.objects.filter(id=culture_id).first()
            if culture_obj:
                form = CultureCreatePostForm(instance=culture_obj)
            else:
                form = CultureCreatePostForm()
        else:  # Add mode
            form = CultureCreatePostForm()
    context = {
        "form": form,
        "culture_obj": culture_obj
    }
    return render(request, 'Samaj/culture_create_post.html', context)


def support(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        if full_name and message and email and phone_number:
            Support.objects.create(full_name = full_name, email = email, phone_number=phone_number, message = message)
            messages.success(request, 'support request submitted successfully!')
        else:
            messages.error(request, 'All fields are required. Please complete the form.')
        return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
    return render(request, 'Samaj/support.html')


