from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from beauty.models.service import Category, Service, Shop, Blog
from beauty.serializers.service import (CategoryModelSerializer, ServiceModelSerializer, ServiceListSerializer,
                                        ShopModelSerializer, BlogModelSerializer, BlogDetailModelSerializer,
                                        ShopDetailModelSerializer)


class CategoryListCreateAPIView(ListAPIView):
    """
    API for listing and creating a new category

    Example Request Body:
    """
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)


class ServiceByCategoryAPIView(ListAPIView):
    """
    API for listing services by category
    """
    serializer_class = ServiceListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="ID of the category to filter services",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filters the queryset based on category_id
        """
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Service.objects.filter(category_id=category_id)
        return Service.objects.all()


class ServiceCreateAPIView(CreateAPIView):
    """
    API for listing and creating a new service

    Example Request Body:
    """
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)


class ServiceListAPIView(ListAPIView):
    """
    API for listing all services

    Example Request Body:

    ## search: service_name, master_full_name, category_name

    """
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'user__username', 'category__name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('user_id')
        category_id = self.request.query_params.get('category_id')
        if user_id and category_id:
            self.queryset = Service.objects.filter(user_id=user_id, category_id=category_id)
        elif user_id:
            self.queryset = Service.objects.filter(user_id=user_id)
        elif category_id:
            self.queryset = Service.objects.filter(category_id=category_id)
        else:
            self.queryset = Service.objects.all()
        return super().get(request, *args, **kwargs)


class ServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API for retrieving, updating and deleting a service

    Example Request Body:
    """
    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Service.objects.filter(user=self.request.user)
        else:
            return Service.objects.none()


# class ServiceSearchListAPIView(ListAPIView):
#     """
#     API for searching services
#
#     Example Request Body:
#
#     ### service_name
#     ### master_username
#     ### category_name
#     """
#     queryset = Service.objects.all()
#     serializer_class = ServiceListSerializer
#     filter_backends = [SearchFilter, DjangoFilterBackend]
#     search_fields = ["name", "user__username", "category__name"]
#     permission_classes = (AllowAny,)


class ShopListAPIView(ListAPIView):
    """
    API for listing all shops

    Example Request Body:
    """
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    # filter_backends = [SearchFilter, DjangoFilterBackend]
    # search_fields = ['name', 'user__username', 'category__name']


class ShopRetrieveAPIView(RetrieveAPIView):
    """
    API for retrieving a shop and incrementing the view count
    """
    queryset = Shop.objects.all()
    serializer_class = ShopDetailModelSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class BlogListAPIView(ListAPIView):
    """
    API for listing all blogs

    Example Request Body:
    """
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer


class BlogRetrieveApiView(RetrieveAPIView):
    """
    API for retrieving a blog

    Example Request Body:
    """
    queryset = Blog.objects.all()
    serializer_class = BlogDetailModelSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)
