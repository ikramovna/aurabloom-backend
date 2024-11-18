from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from beauty.models.favorite import Favorite, Saved, ShopFavorite
from beauty.models.service import Category, Service, Blog
from users.serializers import UserServiceModelSerializer


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class ServiceModelSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField(required=False)

    class Meta:
        model = Service
        fields = ('id', 'name', 'price', 'duration', 'description', 'category', "image", 'user')

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_master:
            raise serializers.ValidationError('Only master can add posts')
        return attrs


class ServiceListSerializer(ModelSerializer):
    user = UserServiceModelSerializer()
    favorites_count = serializers.SerializerMethodField()

    is_like = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'id', 'name', 'price', "image", 'category', 'duration', 'description', 'user', 'favorites_count', 'is_like',
            'is_saved')

    def get_favorites_count(self, obj):
        return Favorite.objects.filter(service=obj).count()

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(service=obj, user=user).exists()
        return False

    def get_is_saved(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Saved.objects.filter(service=obj, user=user).exists()
        return False


class ShopModelSerializer(ModelSerializer):
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = ('id', 'name', 'price', 'description', 'image', 'like_count')

    def get_like_count(self, obj):
        return ShopFavorite.objects.filter(product=obj).count()


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'description', 'image1', 'image2', 'image3', 'image4', 'created_at')
