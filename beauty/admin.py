from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from beauty.models.about import Faq, About, AboutImage
from beauty.models.booking import Time, WorkingDays, Booking
from beauty.models.favorite import Favorite, Saved, ShopSaved, ShopFavorite
from beauty.models.region import Region, District, Mahalla
from beauty.models.service import Category, Service, Shop, Blog


@admin.register(Region)
class RegionModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    filter = ("name",)
    ordering = ("id",)


@admin.register(District)
class DistrictModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "region")
    ordering = ("id",)


@admin.register(Mahalla)
class MahallaModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "district")
    ordering = ("id",)


@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "image")


@admin.register(Service)
class CategoryModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "price", "duration", "description", "category", "user")


@admin.register(Favorite)
class FavoriteModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "service", "user", "like")


@admin.register(Saved)
class SavedModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "service", "user", "saved")


@admin.register(WorkingDays)
class WorkingDaysModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "day")
    ordering = ("id",)


@admin.register(Time)
class WorkingTimeModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "day", "start_time", "end_time", "user")
    ordering = ("id",)


@admin.register(Booking)
class BookingModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "date", "time", "user", "status")
    ordering = ("id",)


@admin.register(Faq)
class FaqModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "question", "answer")
    ordering = ("id",)


@admin.register(About)
class AboutModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "title", "description")
    ordering = ("id",)


@admin.register(AboutImage)
class AboutImageModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "image")
    ordering = ("id",)


@admin.register(Shop)
class ShopModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "price", "description", "availability", "view")
    ordering = ("id",)


@admin.register(ShopSaved)
class ShopSavedModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "product", "user", "saved")
    ordering = ("id",)


@admin.register(ShopFavorite)
class ShopFavoriteModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "product", "user", "like")
    ordering = ("id",)


@admin.register(Blog)
class BlogModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "title", "description", "image1", "image2", "image3", "image4", "created_at", "view")
    ordering = ("id",)
