from django.db.models import *


class Faq(Model):
    question = CharField(max_length=255)
    answer = TextField()

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        db_table = "faq"

    def __str__(self):
        return self.question


class AboutImage(Model):
    image = ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = "About Us Image"
        verbose_name_plural = "About Us Images"
        db_table = "about_image"

    # def __str__(self):
    #     return self.image


class About(Model):
    title = CharField(max_length=255)
    description = TextField()
    image = ManyToManyField(AboutImage, blank=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        db_table = "about_us"

    def __str__(self):
        return self.title