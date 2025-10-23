from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone

from booking.models import Booking


@login_required(login_url='/auth/login/')
def profile_dashboard(request):
    profile = request.user.profile
    today = timezone.localdate()

    bookings_queryset = (
        profile.bookings.select_related('venue', 'venue__city')
        .order_by('date', 'start_time')
    )

    upcoming_bookings = bookings_queryset.filter(date__gte=today)
    past_bookings = bookings_queryset.filter(date__lt=today).order_by('-date', '-start_time')

    owned_venues = []
    owner_upcoming_total = 0

    if profile.is_owner:
        venue_bookings_prefetch = Prefetch(
            'bookings',
            queryset=(
                Booking.objects.filter(date__gte=today)
                .select_related('user__user')
                .order_by('date', 'start_time')
            ),
            to_attr='upcoming_bookings',
        )

        owned_venues = (
            profile.venues.all()
            .select_related('city', 'category')
            .prefetch_related(venue_bookings_prefetch)
        )

        owner_upcoming_total = sum(len(venue.upcoming_bookings) for venue in owned_venues)

    context = {
        'profile': profile,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings[:5],
        'past_bookings_count': past_bookings.count(),
        'owned_venues': owned_venues,
        'owner_upcoming_total': owner_upcoming_total,
        'today': today,
    }

    return render(request, 'account/profile_dashboard.html', context)
