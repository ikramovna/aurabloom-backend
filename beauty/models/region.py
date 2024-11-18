from django.db.models import *


class Region(Model):
    name = CharField(max_length=255)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        db_table = "region"

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE, related_name='district')

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        db_table = "district"

    def __str__(self):
        return self.name


class Mahalla(Model):
    name = CharField(max_length=255)
    district = ForeignKey('District', CASCADE, related_name='mahalla')

    class Meta:
        verbose_name = "Neighborhood"
        verbose_name_plural = "Neighborhoods"
        db_table = "mahalla"

    def __str__(self):
        return self.name


class Address(Model):
    region = ForeignKey('Region', CASCADE, related_name='address')
    district = ForeignKey('District', CASCADE, related_name='address')
    mahalla = ForeignKey('Mahalla', CASCADE, related_name='address')
    house = CharField(max_length=255)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "address"

    def __str__(self):
        return f"{self.region} {self.district} {self.mahalla} {self.house}"
