from django.shortcuts import render


def index(request):
    return render(request, 'Samaj/index.html')


def bio_data(request):
    return render(request, 'Samaj/bio_data.html')


def community(request):
    return render(request, 'Samaj/community.html')


def my_family(request):
    return render(request, 'Samaj/my_family.html')


def news_and_events(request):
    return render(request, 'Samaj/news_and_events.html')
