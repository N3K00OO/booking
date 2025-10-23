from django.urls import path
from landing.views import (
    show_landing, features_preview, header_test, features_review, booking_preview
)

app_name = 'landing'

urlpatterns = [
    path('', show_landing, name='show_landing'),
    path('features/', features_preview, name='features_preview'),
    path('header/', header_test, name='header_test'),
    path('review/', features_review, name='features_review'),
    path('booking-preview/', booking_preview, name='booking_preview'),
]