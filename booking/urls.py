from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('me/', views.user_bookings, name='user_bookings'),
    path('venue/<int:venue_id>/availability/', views.get_availability, name='venue_availability'),
    path('venue/<int:venue_id>/book/', views.create_booking, name='create_booking'),
]
