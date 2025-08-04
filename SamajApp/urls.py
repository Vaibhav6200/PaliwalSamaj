from django.urls import path
from .views import *

app_name = 'samaj'

urlpatterns = [
    path('', index, name='index'),
    path('login/', site_login, name='site_login'),
    path('logout/', site_logout, name='site_logout'),
    path('reset_member_password/', reset_member_password, name='reset_member_password'),

    path('community/', community, name='community'),
    path('news_and_events/', news_and_events, name='news_and_events'),
    path('news_events_detail/<slug:event_slug>/', news_events_detail, name='news_events_detail'),

    path('bio_data/', bio_data, name='bio_data'),
    path('handle_bio_data_form/<slug:family_code>/', handle_bio_data_form, name='handle_bio_data_form'),
    path('handle_member_delete/', handle_member_delete, name='handle_member_delete'),

    path('my_family/', my_family, name='my_family'),
    path('family_tree/<int:member_id>/', member_family_tree, name='member_family_tree'),

    path('sandesh/', sandesh, name='sandesh'),
    path('user_profile/<int:member_id>/', user_profile, name='user_profile'),

    path('newsletter_subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('suggestions/', suggestions, name='suggestions'),
    path('get_member_search_list/', get_member_search_list, name='get_member_search_list'),
    path('image_and_video_gallery/', image_and_video_gallery, name='image_and_video_gallery'),

    path('culture_detail/<slug:culture_slug>', culture_details, name='culture_detail'),
]
