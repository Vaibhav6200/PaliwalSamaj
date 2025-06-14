from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from SamajApp.models import NewsEvent, Comment, Member, Family, Newsletter, QualificationDetail, OccupationDetail
from django.contrib import messages
from .utils import generate_username


def index(request):
    news_events_obj = NewsEvent.objects.all()
    context = {
        'news_and_events': news_events_obj,
    }
    return render(request, 'Samaj/index.html', context)


@login_required
def bio_data(request):
    context = {
        'family_code': Member.objects.get(user=request.user).family.family_code
    }
    return render(request, 'Samaj/bio_data.html', context)


@login_required
def handle_bio_data_form(request, family_code):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        curr_user = User.objects.create(
            username = generate_username(first_name, last_name),
            first_name = first_name,
            last_name = last_name,
            email = request.POST.get('email', None),
        )

        member = Member(
            family = Family.objects.get(family_code=family_code),
            user = curr_user,
            father_name = request.POST.get('father_name'),
            mother_name = request.POST.get('mother_name'),
            date_of_birth = request.POST.get('date_of_birth'),
            birth_place = request.POST.get('birth_place'),
            birth_time = request.POST.get('birth_time'),
            gender = request.POST.get('gender'),
            marital_status = request.POST.get('marital_status'),
            height = request.POST.get('height'),
            phone_number = request.POST.get('phone_number'),
            whatsapp_number = request.POST.get('whatsapp_number'),
            gotra = request.POST.get('gotra'),
            current_address = request.POST.get('address'),
            profile_image = request.FILES.get('profileImage'),
            qualification_type = request.POST.get('qualification'),
            occupation_type = request.POST.get('occupation'),
            instagram_link = request.POST.get('instagram_link'),
            facebook_link = request.POST.get('facebook_link'),
        )
        member.save()

        QualificationDetail.objects.create(
            member = member,
            class_name = request.POST.get('school_class'),
            school_name = request.POST.get('school_name', None),
            college_name = request.POST.get('college_name'),
            degree_name = request.POST.get('degree_name')
        )

        OccupationDetail.objects.create(
            member = member,
            company_name = request.POST.get('company_name'),
            company_location = request.POST.get('job_location'),
            job_description = request.POST.get('job_description'),
            business_name = request.POST.get('business_name'),
            business_location = request.POST.get('business_location'),
            business_description = request.POST.get('business_description')
        )

        messages.success(request, 'Member Added Successfully')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))


@login_required
def handle_edit_bio_data_form(request, family_code):
    if request.method == 'POST':
        family = Family.objects.get(family_code=family_code)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        date_of_birth = request.POST.get('date_of_birth')
        birth_place = request.POST.get('birth_place')
        birth_time = request.POST.get('birth_time')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        height = request.POST.get('height')
        phone_number = request.POST.get('phone_number')
        whatsapp_number = request.POST.get('whatsapp_number')
        gotra = request.POST.get('gotra')
        current_address = request.POST.get('address')
        profile_image = request.FILES.get('profileImage')
        qualification_type = request.POST.get('qualification')
        occupation_type = request.POST.get('occupation')
        instagram_link = request.POST.get('instagram_link')
        facebook_link = request.POST.get('facebook_link')
        class_name = request.POST.get('school_class')
        school_name = request.POST.get('school_name', None)
        college_name = request.POST.get('college_name')
        degree_name = request.POST.get('degree_name')
        company_name = request.POST.get('company_name')
        company_location = request.POST.get('job_location')
        job_description = request.POST.get('job_description')
        business_name = request.POST.get('business_name')
        business_location = request.POST.get('business_location')
        business_description = request.POST.get('business_description')

        messages.success(request, 'Profile Updated Successfully')
    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))



def community(request):
    return render(request, 'Samaj/community.html')


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