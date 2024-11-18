from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from beauty.models.region import Region, District, Address, Mahalla


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class MahallaModelSerializer(ModelSerializer):
    class Meta:
        model = Mahalla
        fields = ('id', 'name', 'district')


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'region', 'district', 'mahalla', 'house')

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "region": instance.region.name,
            "district": instance.district.name,
            "mahalla": instance.mahalla.name,
            "house": instance.house
        }
