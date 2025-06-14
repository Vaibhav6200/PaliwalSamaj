from django.urls import path
from .views import *

app_name = 'samaj'

urlpatterns = [
    path('', index, name='index'),
    path('login/', site_login, name='site_login'),
    path('community/', community, name='community'),
    path('news_and_events/', news_and_events, name='news_and_events'),
    path('news_events_detail/<slug:event_slug>/', news_events_detail, name='news_events_detail'),

    path('bio_data/', bio_data, name='bio_data'),
    path('handle_bio_data_form/<slug:family_code>/', handle_bio_data_form, name='handle_bio_data_form'),
    path('my_family/', my_family, name='my_family'),

    path('sandesh/', sandesh, name='sandesh'),
    path('user_profile/', user_profile, name='user_profile'),


    path('paliwal_samaj_history/', paliwal_samaj_history, name='paliwal_samaj_history'),
    path('karyarat_sangathan/', karyarat_sangathan, name='karyarat_sangathan'),
    path('sandhya_vandana/', sandhya_vandana, name='sandhya_vandana'),
    path('brahman_16_sanskar/', brahman_16_sanskar, name='brahman_16_sanskar'),
    path('upanayan_sanskar/', upanayan_sanskar, name='upanayan_sanskar'),
    path('mewar_paliwal_samaj_ke_teerth_purohit/', mewar_paliwal_samaj_ke_teerth_purohit, name='mewar_paliwal_samaj_ke_teerth_purohit'),
    path('vivah_karyakram/', vivah_karyakram, name='vivah_karyakram'),
    path('vivah_geet/', vivah_geet, name='vivah_geet'),
    path('antyeshti_kriya_paddhati/', antyeshti_kriya_paddhati, name='antyeshti_kriya_paddhati'),
    path('dasva_gyarahva_evam_barahva_karyakram/', dasva_gyarahva_evam_barahva_karyakram, name='dasva_gyarahva_evam_barahva_karyakram'),

    path('newsletter_subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('suggestions/', suggestions, name='suggestions'),
]
