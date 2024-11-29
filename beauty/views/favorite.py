from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from beauty.models.favorite import Favorite, Saved, ShopFavorite, ShopSaved
from beauty.models.service import Shop
from beauty.serializers.favorite import FavoriteSerializer, SavedSerializer, ShopFavoriteSerializer, ShopSavedSerializer


class FavoriteListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows users to create and list their favorite services.

    Example of request:
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def get_likes_count(self, service_id):
        return Favorite.objects.filter(service_id=service_id, like=True).count()

    def post(self, request, *args, **kwargs):
        service_id = request.data.get('service')
        user = request.user
        like_value = request.data.get('like', True)

        if like_value is False:
            Favorite.objects.filter(service_id=service_id, user=user).delete()
            return Response({
                'id': user.id,
                'service': service_id,
                'like': False,
                'message': 'Favorite  deleted successfully'
            })

        favorite_instance, created = Favorite.objects.get_or_create(
            service_id=service_id,
            user=user,
            defaults={'like': like_value}
        )

        if not created and favorite_instance.like != like_value:
            favorite_instance.like = like_value
            favorite_instance.save()

        likes_count = self.get_likes_count(service_id)
        serializer = self.get_serializer(favorite_instance)
        response_data = serializer.data
        response_data['likes_count'] = likes_count
        response_data['message'] = 'Favorite  created successfully'
        return Response(response_data)


class SavedListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows users to create and list their saved services.

    Example of request:
    """
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Saved.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        service_id = request.data.get('service')
        user = request.user
        saved_value = request.data.get('saved', True)

        if saved_value is False:
            Saved.objects.filter(service_id=service_id, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        saved_instance, created = Saved.objects.get_or_create(
            service_id=service_id,
            user=user,
            defaults={'saved': saved_value}
        )

        if not created and saved_instance.saved != saved_value:
            saved_instance.saved = saved_value
            saved_instance.save()

        serializer = self.get_serializer(saved_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ShopFavoriteListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows users to create and list their favorite shops.
    """
    queryset = ShopFavorite.objects.all()
    serializer_class = ShopFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ShopFavorite.objects.filter(user=user)

    def get_likes_count(self, shop):
        return ShopFavorite.objects.filter(product=shop, like=True).count()

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        user = request.user
        like_value = request.data.get('like', True)

        try:
            shop = Shop.objects.get(id=product_id)
        except Shop.DoesNotExist:
            return Response({'error': 'Shop not found'}, status=404)

        if like_value is False:
            ShopFavorite.objects.filter(product=shop, user=user).delete()
            return Response({
                'id': user.id,
                'product': product_id,
                'like': False,
                'message': 'Favorite deleted successfully'
            })

        favorite_instance, created = ShopFavorite.objects.get_or_create(
            product=shop,
            user=user,
            defaults={'like': like_value}
        )

        if not created and favorite_instance.like != like_value:
            favorite_instance.like = like_value
            favorite_instance.save()

        likes_count = self.get_likes_count(shop)
        serializer = self.get_serializer(favorite_instance)
        response_data = serializer.data
        response_data['likes_count'] = likes_count
        response_data['message'] = 'Favorite created successfully'
        return Response(response_data)


class ShopSavedListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows users to create and list their saved shops.
    """
    queryset = ShopSaved.objects.all()
    serializer_class = ShopSavedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ShopSaved.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        user = request.user
        saved_value = request.data.get('saved', True)

        # Handle deletion if saved is set to False
        if saved_value is False:
            ShopSaved.objects.filter(product_id=product_id, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        saved_instance, created = ShopSaved.objects.get_or_create(
            product_id=product_id,
            user=user,
            defaults={'saved': saved_value}
        )

        if not created and saved_instance.saved != saved_value:
            saved_instance.saved = saved_value
            saved_instance.save()

        serializer = self.get_serializer(saved_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
