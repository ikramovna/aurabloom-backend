from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from beauty.models.about import Faq, About
from beauty.models.service import Service
from beauty.serializers.about import AboutModelSerializer, FaqModelSerializer
from beauty.serializers.service import ServiceListSerializer


class FaqAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqModelSerializer
    queryset = Faq.objects.all()

    @swagger_auto_schema(operation_description="Frequently Asked Questions")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AboutAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AboutModelSerializer
    queryset = About.objects.all()

    @swagger_auto_schema(operation_description="About Us")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SearchServiceByNameView(ListAPIView):
    serializer_class = ServiceListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Auction name to search for",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        name_query = self.request.query_params.get('name', None)
        if not name_query:
            return Response({"error": "The 'name' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Service.objects.filter(name__icontains=name_query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
