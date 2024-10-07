# length/urls.py
from django.urls import path
from .views import PipeLengthView, PipeLengthListView

app_name = 'length'

urlpatterns = [
    path('', PipeLengthView.as_view(), name='length'),
    path('length_list/', PipeLengthListView.as_view(), name='length_list'),
]
