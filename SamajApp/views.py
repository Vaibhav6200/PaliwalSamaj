from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from SamajApp.models import NewsEvent, Comment, Member, Family, ClientSubscription
from django.contrib import messages


def index(request):
    news_events_obj = NewsEvent.objects.all()
    context = {
        'news_and_events': news_events_obj,
    }
    return render(request, 'Samaj/index.html', context)


def bio_data(request):
    return render(request, 'Samaj/bio_data.html')


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


def newsletter(request):
    if request.method == "POST":
        client_email = request.POST.get('email')
        if client_email:
            ClientSubscription.objects.get_or_create(email=client_email)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
    return None
