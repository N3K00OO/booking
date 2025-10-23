from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from booking.models import Booking
from venue.models import Category, City, Venue


class ProfileDashboardViewTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Jakarta')
        self.category = Category.objects.create(name='Futsal')

        self.user = User.objects.create_user(
            username='member',
            password='password123',
            first_name='Alya',
        )
        self.user_profile = self.user.profile

        self.owner = User.objects.create_user(
            username='owner',
            password='password123',
            first_name='Fakhri',
        )
        self.owner_profile = self.owner.profile
        self.owner_profile.role = 'OWNER'
        self.owner_profile.save()

        self.venue = Venue.objects.create(
            owner=self.owner_profile,
            name='Arena Utama',
            price=120000,
            city=self.city,
            category=self.category,
            type='Indoor',
            address='Jl. Sudirman No. 1',
            description='Lapangan futsal berstandar nasional.',
            image_url='https://example.com/arena.jpg',
        )

        future_date = timezone.localdate() + timedelta(days=3)
        self.booking = Booking.objects.create(
            user=self.user_profile,
            venue=self.venue,
            date=future_date,
            start_time=time(9, 0),
            duration_hours=2,
        )

    def test_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('account:profile_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login/'))

    def test_user_sees_upcoming_bookings(self):
        logged_in = self.client.login(username='member', password='password123')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('account:profile_dashboard'))
        self.assertEqual(response.status_code, 200)

        upcoming = list(response.context['upcoming_bookings'])
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].id, self.booking.id)

    def test_owner_context_includes_owned_venues(self):
        logged_in = self.client.login(username='owner', password='password123')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('account:profile_dashboard'))
        self.assertEqual(response.status_code, 200)

        owned_venues = list(response.context['owned_venues'])
        self.assertEqual(len(owned_venues), 1)
        self.assertEqual(owned_venues[0].id, self.venue.id)
        self.assertEqual(len(owned_venues[0].upcoming_bookings), 1)
        self.assertEqual(response.context['owner_upcoming_total'], 1)
