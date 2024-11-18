from datetime import datetime, timedelta

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import HiddenField, CurrentUserDefault

from beauty.models.booking import Time, Booking, WorkingDays
from beauty.models.region import Address
from beauty.models.service import Service
from beauty.serializers.service import ServiceModelSerializer
from root import settings
from users.models import User
from users.serializers import UserModelSerializer


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDays
        fields = ('id', 'day')


class TimeSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Time
        fields = ('id', 'day', 'start_time', 'end_time', 'user')

    def validate(self, attrs):
        day = attrs.get('day')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time >= end_time:
            raise serializers.ValidationError("The start time must be less than the end time")

        # if Time.objects.filter(day=day, start_time=start_time, end_time=end_time).exists():
        #     raise serializers.ValidationError("The time slot already exists")

        return attrs


class MasterFreeTimeSerializer(serializers.Serializer):
    date = serializers.DateField()
    service_ids = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        date = attrs.get('date')
        service_ids = attrs.get('service_ids')

        if date < timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the past")

        if not service_ids:
            raise serializers.ValidationError("No service id provided")

        for service_id in service_ids:
            try:
                Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                raise serializers.ValidationError(f"Service with ID {service_id} not found")

        if date < timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the past")

        day_index = date.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = days[day_index]

        for service_id in service_ids:
            service = Service.objects.get(id=service_id)
            master_working_time = Time.objects.filter(user=service.user, day__day=day)

            if not master_working_time.exists():
                raise serializers.ValidationError("The requested date is not a working day for the master")

        return attrs

    def get_free_times(self):
        date = self.validated_data['date']
        service_ids = self.validated_data['service_ids']
        day_index = date.weekday()
        total_duration = timedelta()

        for service_id in service_ids:
            service = Service.objects.get(id=service_id)
            hours, minutes = map(int, service.duration.split(":"))
            total_duration += timedelta(hours=hours, minutes=minutes)

        time_slots = []
        for service_id in service_ids:
            service = Service.objects.get(id=service_id)
            time_slots.extend(service.user.time_user.filter(day=day_index))

        bookings = Booking.objects.filter(date=date)

        booked_times = set()

        for booking in bookings:
            booked_times.add(booking.time)

        free_times = set()

        for time_slot in time_slots:
            start_time = datetime.strptime(time_slot.start_time, "%H:%M").time()
            end_time = datetime.strptime(time_slot.end_time, "%H:%M").time()
            start = datetime.combine(date, start_time)
            end = datetime.combine(date, end_time)
            num_intervals = int((end - start) / total_duration)

            for i in range(num_intervals):
                interval_start = start + i * total_duration
                interval_end = interval_start + total_duration

                interval_start_time = interval_start.time().strftime("%H:%M")
                if interval_start_time not in booked_times:
                    free_times.add(interval_start_time)

        free_times_list = sorted(list(free_times))

        return free_times_list


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    service_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'date', 'time', 'service_ids', 'user', 'status')

    def validate(self, attrs):
        date = attrs.get('date')
        time = attrs.get('time')
        service_ids = attrs.get('service_ids', [])
        current_date = timezone.now().date()
        current_time = timezone.now().time()

        for service_id in service_ids:
            if not Service.objects.filter(pk=service_id).exists():
                raise serializers.ValidationError(f"Service with ID {service_id} does not exist")

        day_index = date.weekday()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = days[day_index]

        for service_id in service_ids:
            service = Service.objects.get(id=service_id)
            master_working_time = Time.objects.filter(user=service.user, day__day=day)

            if not master_working_time.exists():
                raise serializers.ValidationError("The requested date is not a working day for the master")

        if not service_ids:
            raise serializers.ValidationError({"service_ids": ["At least one service must be selected"]})
        if not all(isinstance(service_id, int) for service_id in service_ids):
            raise serializers.ValidationError({"service_ids": ["All service IDs must be integers"]})

        services = Service.objects.filter(pk__in=service_ids)

        if len(services) != len(service_ids):
            raise serializers.ValidationError({"service_ids": ["One or more services do not exist"]})

        if Booking.objects.filter(date=date, time=time, service__in=services).exists():
            raise serializers.ValidationError("The requested date, time, and service combination is already booked")

        if date < current_date:
            raise serializers.ValidationError("The date cannot be in the past")
        if date == current_date and datetime.strptime(time, "%H:%M").time() < current_time:
            raise serializers.ValidationError("The time cannot be in the past")

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['service'] = ServiceModelSerializer(instance.service.all(), many=True).data
        return representation

    def create(self, validated_data):
        service_ids = validated_data.pop('service_ids', [])
        booking = Booking.objects.create(**validated_data)

        for service_id in service_ids:
            service = Service.objects.get(pk=service_id)
            booking.service.add(service)

        return booking


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'status')

    def validate(self, attrs):
        status = attrs.get('status')

        if status not in Booking.StatusChoices.values:
            raise serializers.ValidationError("Invalid status")

        return attrs

    @staticmethod
    def send_booking_status_email(instance):
        print("send_booking_status_email method has been called")
        user = instance.user
        subject = f"Booking {instance.status.capitalize()}"
        html_content = render_to_string('booking_email_template.html',
                                        {'status': instance.status, 'user': user, 'booking_status': instance.status})
        text_content = strip_tags(html_content)
        from_email = f"AURA TEAM <{settings.EMAIL_HOST_USER}>"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        print("Sending email...")
        email.send()
        print("Email sent.")

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.send_booking_status_email(instance)
        return instance



    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #
    #     if not request.user.is_master or not instance.service.filter(user=request.user).exists():
    #         raise PermissionDenied("You do not have permission to update this booking")
    #     return super().update(instance, validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'duration', 'price')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'region', 'district', 'mahalla', 'house')
        ref_name = 'BookingAddress'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'region': instance.region.name,
            'district': instance.district.name,
            'mahalla': instance.mahalla.name,
            'house': instance.house
        }


class UserServiceSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'address', 'image', 'is_master')


class MyBookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=True)
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'date', 'time', 'service', 'status', 'user')
