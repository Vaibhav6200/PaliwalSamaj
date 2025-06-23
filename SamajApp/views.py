from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from SamajApp.models import NewsEvent, Comment, Member, Family, Newsletter, QualificationDetail, OccupationDetail, \
    Suggestion, SamajMemberRoles, Sandesh, Gallery, Culture
from django.contrib import messages
from .utils import generate_username, MessageHandler, calculate_age
from datetime import date, timedelta
from django.core.paginator import Paginator
from .tasks import translate_member_fields
from django.utils import translation


def site_login(request):
    return render(request, 'Samaj/login.html')


def index(request):
    news_events_obj = NewsEvent.objects.all()

    netritva_mandal = SamajMemberRoles.objects.filter(
        Q(role='adhyaksh')|
        Q(role='upadhyaksh')|
        Q(role='sachiv') |
        Q(role='koshadhyaksh')
    )
    sanchalan_samiti = SamajMemberRoles.objects.filter(
        Q(role='mahila_adhyaksh')|
        Q(role='saha_sachiv') |
        Q(role='sanrakshak')
    )
    aayojan_mandal = SamajMemberRoles.objects.filter(
        Q(role='salahkaar') |
        Q(role='aayojan_samiti')
    )
    karyakarini_sadasya = SamajMemberRoles.objects.filter(role='karyakari_sadasya')

    context = {
        'news_and_events': news_events_obj,
        'netritva_mandal': netritva_mandal,
        'sanchalan_samiti': sanchalan_samiti,
        'aayojan_mandal': aayojan_mandal,
        'karyakarini_sadasya': karyakarini_sadasya,
    }
    return render(request, 'Samaj/index.html', context)


@login_required
def bio_data(request):
    context = {
        'family_code': Member.objects.get(user=request.user).family.family_code,
        'gotras': Member.GOTRA_CHOICES,
        'degrees': QualificationDetail.DEGREE_CHOICES,
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
            user.email = email
            user.save()
            member, _ = Member.objects.get_or_create(user=user, family=family)
            messages.success(request, 'Profile Updated Successfully')
        else:
            # CREATE FLOW
            user = User(username=generate_username(full_name))
            if email:
                user.email=email
            user.save()
            member = Member(user=user, family=family)
            messages.success(request, 'Member Added Successfully')

        member.full_name = full_name
        member.father_name = request.POST.get('father_name')
        member.mother_name = request.POST.get('mother_name')
        member.birth_place = request.POST.get('birth_place')
        member.current_address = request.POST.get('address')
        member.current_address_city = request.POST.get('city')
        member.current_address_state = request.POST.get('state')

        member.date_of_birth = request.POST.get('date_of_birth')
        member.birth_time = request.POST.get('birth_time')
        member.gender = request.POST.get('gender')
        member.marital_status = request.POST.get('marital_status')
        member.height = request.POST.get('height')
        member.phone_number = request.POST.get('phone_number')
        member.whatsapp_number = request.POST.get('whatsapp_number')
        member.gotra = request.POST.get('gotra')
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
        if member.qualification_type == 'school':
            school_class = request.POST.get('school_class')
            qualification.school_class = int(school_class) if school_class else None
            qualification.school_name = request.POST.get('school_name')
            qualification.college_name = None
            qualification.degree_name = None
        else:
            qualification.school_class = None
            qualification.school_name = None
            qualification.college_name = request.POST.get('college_name')
            qualification.degree_name = request.POST.get('degree_name')
        qualification.save()

        # Occupation Details
        occupation, _ = OccupationDetail.objects.get_or_create(member=member)
        if member.occupation_type == 'job':
            occupation.company_name = request.POST.get('company_name')
            occupation.company_location = request.POST.get('job_location')
            occupation.job_description = request.POST.get('job_description')

            # Clear business fields
            occupation.business_name = None
            occupation.business_location = None
            occupation.business_description = None

        elif member.occupation_type == 'business':
            occupation.business_name = request.POST.get('business_name')
            occupation.business_location = request.POST.get('business_location')
            occupation.business_description = request.POST.get('business_description')

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
        current_language = translation.get_language()
        translate_member_fields.delay(member.id, current_language)

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
    context = {
        'min_age_default_value': 10,
        'max_age_default_value': 50,
        'gotras': Member.GOTRA_CHOICES,
        'degrees': QualificationDetail.DEGREE_CHOICES,
    }

    community_members = Member.objects.all()
    if request.method == 'GET':
        name = request.GET.get('name')
        min_age_value = request.GET.get('min_age_value')
        max_age_value = request.GET.get('max_age_value')
        gotra = request.GET.get('gotra')
        gender = request.GET.get('gender')
        education = request.GET.get('education')
        village = request.GET.get('village')
        city = request.GET.get('city')
        state = request.GET.get('state')


        # 🔍 Name filtering (splitting and checking each word in full_name)
        if name:
            name_parts = name.strip().split()
            for part in name_parts:
                community_members = (community_members.filter(user__full_name__icontains=part))

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

        if village:
            community_members = community_members.filter(Q(current_address_village__icontains=village)|Q(current_address__icontains=village))

        if city:
            community_members = community_members.filter(Q(current_address_city__icontains=city)|Q(current_address__icontains=city))

        if state:
            community_members = community_members.filter(Q(current_address_state__icontains=state)|Q(current_address__icontains=state))

    community_members = community_members.order_by('full_name')
    paginator = Paginator(community_members, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['community_members'] = page_obj
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


def member_family_tree(request, member_id):
    community_member = Member.objects.get(id = member_id)
    family_members = Member.objects.filter(family=community_member.family)
    context = {
        'family_head': community_member.family.family_head,
        'family_members': family_members,
    }
    return render(request, 'Samaj/member_family_tree.html', context)


@login_required
def sandesh(request):
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
    member = Member.objects.get(id=member_id)
    context = {
        'profile': member,
        'user_age': calculate_age(member.date_of_birth),
    }
    return render(request, "Samaj/user_profile.html", context)


def news_and_events(request):
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
        message = request.POST.get('message')

        if name and message and email:
            Suggestion.objects.create(name = name, email = email, message = message)
            messages.success(request, 'Thank you! Your suggestion has been submitted.')
        else:
            messages.error(request, 'All fields are required. Please complete the form.')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


@login_required
def handle_login_otp(request):
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
        messages.success(request, f'Password sent to your registered number : {contact_input}')

        # Set login password for user - 6 digit OTP pin

        # if member:
        #     verification_code = random.randint(100000, 999999)
        #     handler = MessageHandler(phone_number=contact_input, otp=verification_code)
        #     handler.send_otp_via_message()
        #     request.session['phone_verification_code'] = verification_code
        #     messages.success(request, f'OTP send to your registered number: {contact_input}')
        # else:
        #     messages.error(request,'This number is not registered in our database.')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


def get_member_search_list(request):
    search_query = request.GET.get('search')
    payload = []
    if search_query:
        words = search_query.strip().split()
        query = Q()
        for word in words:
            query |= Q(phone_number__icontains=word)
            query |= Q(user__full_name__icontains=word)
        objs = Member.objects.filter(query)
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
    context = {
        'years': Gallery.objects.filter(media_type='photo').values_list('year', flat=True).distinct().order_by('-year'),
        'images': Gallery.objects.filter(media_type='photo'),
        'videos': Gallery.objects.filter(media_type='video'),
    }
    return render(request, 'Samaj/image_and_video_gallery.html', context)


def culture_details(request, culture_slug=None):
    culture_obj = Culture.objects.get(slug=culture_slug)
    return render(request, "Samaj/culture_details.html", {'culture': culture_obj})
