from ckeditor.fields import RichTextField
from django.db.models import *
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.name


class Service(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    duration = CharField(max_length=10)
    description = TextField(null=True, blank=True)
    category = ForeignKey(Category, on_delete=CASCADE, related_name='services')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='services')
    image = ImageField(upload_to='service/')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        db_table = 'service'

    def __str__(self):
        return self.name


class Shop(Model):
    name = CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    image = ImageField(upload_to='shop/')
    image1 = ImageField(upload_to='shop/', null=True, blank=True)
    image2 = ImageField(upload_to='shop/', null=True, blank=True)
    image3 = ImageField(upload_to='shop/', null=True, blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    discount = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    view = IntegerField(default=0)
    availability = BooleanField(default=True)



    contact_number = CharField(max_length=20, null=True, blank=True)
    additional_info = RichTextField(null=True, blank=True)
    video = ImageField(upload_to='shop/', null=True, blank=True)
    brand = CharField(max_length=255, null=True, blank=True)
    weight = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size = CharField(max_length=50, null=True, blank=True)
    grams = IntegerField(null=True, blank=True)
    color = CharField(max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
        db_table = 'shop'

    def __str__(self):
        return self.name


class Blog(Model):
    title = CharField(max_length=255)
    description = TextField()
    image1 = ImageField(upload_to='blog/')
    image2 = ImageField(upload_to='blog/', null=True, blank=True)
    image3 = ImageField(upload_to='blog/', null=True, blank=True)
    image4 = ImageField(upload_to='blog/', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    view = IntegerField(default=0)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        db_table = 'blog'

    def __str__(self):
        return self.title
