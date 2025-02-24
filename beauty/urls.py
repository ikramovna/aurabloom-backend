from django.urls import path

from beauty.views.about import FaqAPIView, AboutAPIView, SearchServiceByNameView
from beauty.views.booking import (TimeListCreateAPIView, TimeUpdateDestroyAPIView, MasterFreeTimeListAPIView,
                                  BookingCreateAPIView, WorkingDayListAPIView, MyBookingListAPIView,
                                  BookingUpdateAPIView)
from beauty.views.favorite import (FavoriteListCreateAPIView, SavedListCreateAPIView, ShopFavoriteListCreateAPIView,
                                   ShopSavedListCreateAPIView)
from beauty.views.region import RegionListAPIView, DistrictListAPIView, MahallaListAPIView
from beauty.views.service import (CategoryListCreateAPIView, ServiceCreateAPIView,
                                  ServiceRetrieveUpdateDestroyAPIView, ServiceListAPIView, ServiceByCategoryAPIView,
                                  ShopListAPIView, BlogListAPIView, BlogRetrieveApiView, ShopRetrieveAPIView)

urlpatterns = [
    path("region", RegionListAPIView.as_view()),
    path("district", DistrictListAPIView.as_view()),
    path("mahalla", MahallaListAPIView.as_view()),
    path("category", CategoryListCreateAPIView.as_view()),
    path("favorite", FavoriteListCreateAPIView.as_view()),
    path("saved", SavedListCreateAPIView.as_view()),
    path("service", ServiceCreateAPIView.as_view()),
    path("service/list", ServiceListAPIView.as_view()),
    path("service/<int:pk>", ServiceRetrieveUpdateDestroyAPIView.as_view(), name="service-detail"),
    path("working/day", WorkingDayListAPIView.as_view()),
    path("working/time", TimeListCreateAPIView.as_view()),
    path("working/time/<int:pk>", TimeUpdateDestroyAPIView.as_view()),
    path("booking/<int:pk>", BookingUpdateAPIView.as_view()),
    path("booking", BookingCreateAPIView.as_view()),
    path("booking/time", MasterFreeTimeListAPIView.as_view()),
    path("booking/my", MyBookingListAPIView.as_view()),
    path("faq", FaqAPIView.as_view()),
    path("about", AboutAPIView.as_view()),
    path("category/service", ServiceByCategoryAPIView.as_view()),
    path("shop", ShopListAPIView.as_view()),
    path("shop/<int:pk>", ShopRetrieveAPIView.as_view()),
    path("shop/favorite", ShopFavoriteListCreateAPIView.as_view()),
    path("shop/saved", ShopSavedListCreateAPIView.as_view()),
    path("blog", BlogListAPIView.as_view()),
    path("blog/<int:pk>", BlogRetrieveApiView.as_view()),
    path("search", SearchServiceByNameView.as_view()),

]
