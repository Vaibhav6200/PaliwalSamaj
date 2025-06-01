from django.urls import path
from .views import *

app_name = 'samaj'

urlpatterns = [
    path('', index, name='index'),
    path('community/', community, name='community'),
    path('news_and_events/', news_and_events, name='news_and_events'),
    path('bio_data/', bio_data, name='bio_data'),
    path('my_family/', my_family, name='my_family'),
]
