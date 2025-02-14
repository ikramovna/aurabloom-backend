from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beauty.models.booking import WorkingDays, Time, Booking
from beauty.serializers.booking import (WorkingDaySerializer, TimeSerializer, BookingSerializer,
                                        MasterFreeTimeSerializer, BookingUpdateSerializer, MyBookingSerializer,
                                        UserServiceSerializer, ServiceSerializer)


class WorkingDayListAPIView(ListAPIView):
    """
    API endpoint that allows working days to be viewed.

    Example request:
    """
    queryset = WorkingDays.objects.all()
    serializer_class = WorkingDaySerializer
    permission_classes = (IsAuthenticated,)


class TimeListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows for request user working hours to be viewed or created.

    {
      "times": [
        {
          "day": 1,
          "start_time": "09:00",
          "end_time": "17:00"
        },
        {
          "day": 2,
          "start_time": "10:00",
          "end_time": "18:00"
        }
      ]
    }

    """
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get('times', []), many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Time.objects.filter(user=self.request.user)


class TimeUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    """
    API endpoint that allows for request user working hours to be updated or deleted.

    Example request:
    """
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Time.objects.filter(user=self.request.user)


class MasterFreeTimeListAPIView(ListAPIView):
    """
    API endpoint that allows for master free time to be viewed.

    Example request:
    """
    serializer_class = MasterFreeTimeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description='Date in format YYYY-MM-DD',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('service_ids', openapi.IN_QUERY, description='List of service IDs',
                              type=openapi.TYPE_ARRAY,
                              items=openapi.Items(type=openapi.TYPE_INTEGER))
        ],
    )
    def get(self, request, *args, **kwargs):
        query_params = request.query_params.copy()
        service_ids = query_params.get('service_ids')

        # Validate and convert service_ids to a list of integers
        if service_ids:
            try:
                service_ids = [int(id) for id in service_ids.split(',')]
            except ValueError:
                raise ValidationError("Invalid value for service_ids. Expected a comma-separated list of integers.")

        query_params.setlist('service_ids', service_ids)

        serializer = self.serializer_class(data=query_params)
        serializer.is_valid(raise_exception=True)
        free_times = serializer.get_free_times()
        return Response({"free_times": free_times}, status=200)


class BookingCreateAPIView(CreateAPIView):
    """
    API endpoint that allows for booking to be created.

    Example request:
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)


class BookingUpdateAPIView(UpdateAPIView, DestroyAPIView):
    """
    API endpoint that allows for booking to be updated.

    Example request:
    # pending approved rejected
    """
    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put', 'delete']

    def get_queryset(self):
        if self.request.user.is_master:
            return Booking.objects.filter(service__user=self.request.user)
        return Booking.objects.filter(user=self.request.user)


class BookingStatusFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        if status:
            return queryset.filter(status=status)
        return queryset


class MyBookingListAPIView(ListAPIView):
    """
    API endpoint that allows for request user own booking to be viewed.

    Example request:
    # status = pending, approved, rejected

    """
    serializer_class = MyBookingSerializer
    queryset = Booking.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [BookingStatusFilterBackend]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description='Get booking date in format YYYY-MM-DD',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY, description='Get bookings with a specific status',
                              type=openapi.TYPE_STRING)
        ],
        responses={200: MyBookingSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.is_master:
            master_bookings = queryset.filter(service__user=request.user)
            bookings_data = [{
                'id': booking.id,
                'status': booking.status,
                'date': booking.date,
                'time': booking.time,
                'user': UserServiceSerializer(booking.user).data,
                'service': ServiceSerializer(booking.service.all(), many=True).data
            } for booking in master_bookings]

            master_made_bookings = queryset.filter(user=request.user)
            for booking in master_made_bookings:
                bookings_data.append({
                    'id': booking.id,
                    'status': booking.status,
                    'date': booking.date,
                    'time': booking.time,
                    'user': UserServiceSerializer(booking.service.first().user).data,
                    'service': ServiceSerializer(booking.service.all(), many=True).data
                })
        else:
            user_bookings = queryset.filter(user=request.user)
            bookings_data = [{
                'id': booking.id,
                'status': booking.status,
                'date': booking.date,
                'time': booking.time,
                'service': ServiceSerializer(booking.service.all(), many=True).data,
                'user': UserServiceSerializer(service.user).data
            } for booking in user_bookings for service in booking.service.all()]

        return Response(bookings_data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     if request.user.is_master:
    #         master_bookings = queryset.filter(service__user=request.user)
    #         bookings_data = [{
    #             'id': booking.id,
    #             'status': booking.status,
    #             'date': booking.date,
    #             'time': booking.time,
    #             'user': UserServiceSerializer(booking.user).data,
    #             'service': ServiceSerializer(booking.service.all(), many=True).data
    #         } for booking in master_bookings]
    #
    #         # Fetch the bookings made by the master
    #         master_made_bookings = queryset.filter(user=request.user)
    #         for booking in master_made_bookings:
    #             bookings_data.append({
    #                 'id': booking.id,
    #                 'status': booking.status,
    #                 'date': booking.date,
    #                 'time': booking.time,
    #                 'user': UserServiceSerializer(booking.service.first().user).data,
    #                 'service': ServiceSerializer(booking.service.all(), many=True).data
    #             })
    #     else:
    #         # Fetch the bookings made by the user
    #         user_bookings = queryset.filter(user=request.user)
    #         bookings_data = [{
    #             'id': booking.id,
    #             'status': booking.status,
    #             'date': booking.date,
    #             'time': booking.time,
    #             'service': ServiceSerializer(service).data,
    #             'user': UserServiceSerializer(service.user).data
    #         } for booking in user_bookings for service in booking.service.all()]
    #
    #     return Response(bookings_data)

    # def get_queryset(self):
    #     if self.request.user.is_master:
    #         # Include bookings where the logged-in user is the master of the service that was booked
    #         queryset = Booking.objects.filter(Q(service__user=self.request.user) | Q(user=self.request.user))
    #     else:
    #         queryset = Booking.objects.filter(user=self.request.user)
    #     status = self.request.query_params.get('status')
    #
    #     if status:
    #         queryset = queryset.filter(status=status)
    #
    #     # Include the newly created booking
    #     booking_id = self.request.query_params.get('id')
    #     if booking_id:
    #         queryset = queryset | Booking.objects.filter(id=booking_id)
    #
    #     return queryset
