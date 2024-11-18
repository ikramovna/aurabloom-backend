from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from beauty.models.region import Region, District, Mahalla, Address
from beauty.serializers.region import RegionModelSerializer, DistrictModelSerializer, MahallaModelSerializer, \
    AddressSerializer


class RegionListAPIView(ListAPIView):
    """
    API view for get a regions

    Example Request Body:
    """
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer
    permission_classes = (AllowAny,)


class DistrictListAPIView(ListAPIView):
    """
    API view for get a districts

    ## Enter region_id in the url to get the districts in the desired region
    """
    queryset = District.objects.all()
    serializer_class = DistrictModelSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('region_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        region_id = self.request.query_params.get('region_id')
        if region_id:
            self.queryset = self.queryset.filter(region_id=region_id)
        return super().get(request, *args, **kwargs)


class MahallaListAPIView(ListAPIView):
    """
    API view for get a mahallas

    ## Enter district_id in the url to get the mahallas in the desired district
    """
    queryset = Mahalla.objects.all()
    serializer_class = MahallaModelSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('district_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)])
    def get(self, request, *args, **kwargs):
        district_id = self.request.query_params.get('district_id')
        if district_id:
            self.queryset = self.queryset.filter(district_id=district_id)
        return super().get(request, *args, **kwargs)


