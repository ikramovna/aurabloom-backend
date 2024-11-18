from rest_framework import serializers

from beauty.models.favorite import Favorite, Saved, ShopFavorite, ShopSaved


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('id', 'service', 'user', 'like')

    def validate(self, attrs):
        service = attrs.get('service')
        user = attrs.get('user')

        if Favorite.objects.filter(service=service, user=user).exists():
            raise serializers.ValidationError('You have already added this service to your favorites.')

        return attrs


class SavedSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Saved
        fields = ('id', 'service', 'user', 'saved')

    def validate(self, attrs):
        service = attrs.get('service')
        user = attrs.get('user')

        if Saved.objects.filter(service=service, user=user).exists():
            raise serializers.ValidationError('You have already saved this service.')

        return attrs


class ShopFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShopFavorite
        fields = ('id', 'product', 'user', 'like')

    def validate(self, attrs):
        shop = attrs.get('product')
        user = attrs.get('user')

        if ShopFavorite.objects.filter(shop=shop, user=user).exists():
            raise serializers.ValidationError('You have already added this shop to your favorites.')

        return attrs


class ShopSavedSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShopSaved
        fields = ('id', 'product', 'user', 'saved')

    def validate(self, attrs):
        shop = attrs.get('product')
        user = attrs.get('user')

        if ShopSaved.objects.filter(shop=shop, user=user).exists():
            raise serializers.ValidationError('You have already saved this shop.')

        return attrs
