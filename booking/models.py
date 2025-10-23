from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Booking(models.Model):
    """Represents a reservation for a venue at a specific date and time."""

    MAX_DURATION_HOURS = 8

    user = models.ForeignKey(
        'account.Profile',
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    venue = models.ForeignKey(
        'venue.Venue',
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False, blank=True)
    duration_hours = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_DURATION_HOURS)],
        help_text='Duration of the booking in hours.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['venue', 'date', 'start_time'],
                name='unique_venue_date_start_time',
            )
        ]

    def __str__(self) -> str:
        start = self.start_time.strftime('%H:%M')
        end = self.end_time.strftime('%H:%M')
        return f"{self.venue.name} on {self.date} ({start} - {end})"

    def save(self, *args, **kwargs):  # type: ignore[override]
        self.end_time = self.calculate_end_time()
        super().save(*args, **kwargs)

    def calculate_end_time(self):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(hours=self.duration_hours)
        return end_datetime.time()

    @property
    def total_price(self) -> int:
        return self.duration_hours * self.venue.price
