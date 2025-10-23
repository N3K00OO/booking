import json
from datetime import datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from account.models import Profile
from venue.models import Venue

from .models import Booking


DEFAULT_OPEN_HOUR = 6
DEFAULT_CLOSE_HOUR = 22


def _generate_default_slots():
    return [time(hour=h) for h in range(DEFAULT_OPEN_HOUR, DEFAULT_CLOSE_HOUR)]


def _parse_date(date_string: str):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return None


def _parse_time(time_string: str):
    try:
        return datetime.strptime(time_string, '%H:%M').time()
    except (TypeError, ValueError):
        return None


def _slot_overlaps(slot_start: time, slot_end: time, booking: Booking) -> bool:
    return not (slot_end <= booking.start_time or slot_start >= booking.end_time)


def _calculate_end_time(start: time, duration_hours: int) -> time:
    base_date = datetime.combine(datetime.today(), start)
    end_datetime = base_date + timedelta(hours=duration_hours)
    return end_datetime.time()


def _serialize_booking(booking: Booking) -> dict:
    return {
        'id': booking.id,
        'venue': booking.venue.name,
        'venue_id': booking.venue_id,
        'date': booking.date.isoformat(),
        'start_time': booking.start_time.strftime('%H:%M'),
        'end_time': booking.end_time.strftime('%H:%M'),
        'duration_hours': booking.duration_hours,
        'total_price': booking.total_price,
        'image_url': booking.venue.image_url,
        'city': booking.venue.city.name,
    }


@login_required(login_url='/auth/login/')
def user_bookings(request):
    profile = get_object_or_404(Profile, pk=request.user.pk)
    bookings = (
        profile.bookings.select_related('venue', 'venue__city')
        .order_by('-date', 'start_time')
    )
    context = {
        'bookings': bookings,
        'user_profile': profile,
    }
    return render(request, 'booking/user_bookings.html', context)


@require_http_methods(['GET'])
def get_availability(request, venue_id: int):
    venue = get_object_or_404(Venue, pk=venue_id)
    date_str = request.GET.get('date')
    selected_date = _parse_date(date_str)

    if selected_date is None:
        return JsonResponse({'error': 'Invalid or missing date parameter.'}, status=400)

    existing_bookings = list(
        Booking.objects.filter(venue=venue, date=selected_date)
        .order_by('start_time')
    )

    available_slots = []
    default_slots = _generate_default_slots()

    for slot_start in default_slots:
        slot_end = _calculate_end_time(slot_start, 1)
        conflict = any(_slot_overlaps(slot_start, slot_end, booking) for booking in existing_bookings)
        if not conflict and slot_end > slot_start:
            available_slots.append(slot_start.strftime('%H:%M'))

    response_data = {
        'venue_id': venue.id,
        'date': selected_date.isoformat(),
        'available_start_times': available_slots,
        'booked_slots': [
            {
                'start_time': booking.start_time.strftime('%H:%M'),
                'end_time': booking.end_time.strftime('%H:%M'),
                'duration_hours': booking.duration_hours,
            }
            for booking in existing_bookings
        ],
        'is_fully_booked': len(available_slots) == 0,
    }

    return JsonResponse(response_data)


@login_required(login_url='/auth/login/')
@require_http_methods(['POST'])
def create_booking(request, venue_id: int):
    venue = get_object_or_404(Venue, pk=venue_id)
    profile = get_object_or_404(Profile, pk=request.user.pk)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    date_value = _parse_date(payload.get('date'))
    start_time_value = _parse_time(payload.get('start_time'))
    duration_hours = payload.get('duration_hours')

    if date_value is None or start_time_value is None or duration_hours is None:
        return JsonResponse({'error': 'Missing required fields.'}, status=400)

    try:
        duration_hours = int(duration_hours)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Duration must be an integer.'}, status=400)

    if duration_hours < 1 or duration_hours > Booking.MAX_DURATION_HOURS:
        return JsonResponse({'error': 'Duration is out of allowed range.'}, status=400)

    today = timezone.localdate()
    if date_value < today:
        return JsonResponse({'error': 'Cannot book in the past.'}, status=400)

    if start_time_value.minute != 0:
        return JsonResponse({'error': 'Start time must be on the hour.'}, status=400)

    if start_time_value.hour < DEFAULT_OPEN_HOUR or start_time_value.hour >= DEFAULT_CLOSE_HOUR:
        return JsonResponse({'error': 'Selected start time is outside venue operating hours.'}, status=400)

    end_time_value = _calculate_end_time(start_time_value, duration_hours)
    if end_time_value <= start_time_value or end_time_value.hour > DEFAULT_CLOSE_HOUR:
        return JsonResponse({'error': 'Selected duration exceeds operating hours.'}, status=400)

    overlapping_exists = Booking.objects.filter(
        venue=venue,
        date=date_value,
    ).filter(
        start_time__lt=end_time_value,
        end_time__gt=start_time_value,
    ).exists()

    if overlapping_exists:
        return JsonResponse({'error': 'Selected time slot has already been booked.'}, status=409)

    booking = Booking.objects.create(
        user=profile,
        venue=venue,
        date=date_value,
        start_time=start_time_value,
        duration_hours=duration_hours,
    )

    response_data = {
        'message': 'Booking confirmed!',
        'booking': _serialize_booking(booking),
    }

    return JsonResponse(response_data, status=201)
