from django.urls import path
from venue.views import (
    show_main, show_details, get_venues_json, get_venue_json_by_id, 
    add_venue_ajax, edit_venue_ajax, delete_venue_ajax,
)

app_name = 'venue'

urlpatterns = [
    path('', show_main, name='venue_main'),
    path('detail/<int:id>/', show_details, name='venue_detail'),
    path('api/venues/', get_venues_json, name='api_get_venues'),

    path('api/venue/<int:id>/', get_venue_json_by_id, name='api_get_venue_detail'),
    path('api/venues/add/', add_venue_ajax, name='api_add_venue'),
    path('api/venues/edit/<int:id>/', edit_venue_ajax, name='api_edit_venue'),
    path('api/venues/delete/<int:id>/', delete_venue_ajax, name='api_delete_venue'),
    path('details/<int:id>/', show_details, name='venue_detail'),
]