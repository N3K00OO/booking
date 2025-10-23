from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('venue', 'user', 'date', 'start_time', 'end_time', 'duration_hours')
    list_filter = ('venue', 'date')
    search_fields = ('venue__name', 'user__user__username')
    ordering = ('-date', 'start_time')
