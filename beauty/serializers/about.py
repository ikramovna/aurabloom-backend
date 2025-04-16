from rest_framework.serializers import ModelSerializer

from beauty.models.about import Faq, About, AboutImage, Contact


class FaqModelSerializer(ModelSerializer):
    class Meta:
        model = Faq
        fields = ('id', 'question', 'answer')


class AboutImageModelSerializer(ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ('id', 'image')


class AboutModelSerializer(ModelSerializer):
    image = AboutImageModelSerializer(many=True)

    class Meta:
        model = About
        fields = ('id', 'title', 'description', 'image')


class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'full_name', 'email', 'phone_number', 'message')
