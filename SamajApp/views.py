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