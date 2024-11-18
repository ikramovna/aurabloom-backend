from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from beauty.models.about import Faq, About
from beauty.serializers.about import AboutModelSerializer, FaqModelSerializer


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
