from django.db import models


class Favorite(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorite')
    like = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        db_table = 'favorite'

    def __str__(self):
        return f'{self.user.username} - {self.service.name}'

    @classmethod
    def get_favorites(cls, user):
        return cls.objects.filter(user=user, like=True)

    @classmethod
    def get_total_likes(cls):
        return cls.objects.filter(like=True).count()


class Saved(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Saved'
        verbose_name_plural = 'Saved'
        db_table = 'saved'

    def __str__(self):
        return f'{self.user.username} - {self.service.name}'


class ShopFavorite(models.Model):
    product = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorites')
    like = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Shop Favorite'
        verbose_name_plural = 'Shop Favorite'
        db_table = 'shop_favorite'

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class ShopSaved(models.Model):
    product = models.ForeignKey('Shop', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Shop Saved'
        verbose_name_plural = 'Shop Saved'
        db_table = 'shop_saved'

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
