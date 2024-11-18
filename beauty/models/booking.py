from django.db.models import *

from users.models import User


class WorkingDays(Model):
    day = CharField(max_length=10)

    class Meta:
        verbose_name = 'Working Day'
        verbose_name_plural = 'Working Days'
        db_table = 'working_days'

    def __str__(self):
        return self.day


class Time(Model):
    day = ForeignKey(WorkingDays, on_delete=CASCADE, related_name='time_day')
    start_time = CharField(max_length=10, default='10:00')
    end_time = CharField(max_length=10, default='18:00')
    user = ForeignKey(User, on_delete=CASCADE, related_name='time_user')

    class Meta:
        verbose_name = 'Time'
        verbose_name_plural = 'Times'
        db_table = 'time'

    def __str__(self):
        return f'{self.day} {self.start_time} - {self.end_time}'


class Booking(Model):
    class StatusChoices(TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    date = DateField()
    time = CharField(max_length=10)
    service = ManyToManyField('Service', related_name='booking')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='booking')
    status = CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        db_table = 'booking'

    def __str__(self):
        return f'{self.date} {self.service} {self.user}'
