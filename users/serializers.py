import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from beauty.models.region import Address
from beauty.serializers.region import AddressSerializer
from users.models import User, getKey, setKey
import json

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("full_name", "email", "username", "password", "is_master")

    def validate(self, attrs):
        activate_code = random.randint(100000, 999999)
        user = User(
            full_name=attrs['full_name'],
            email=attrs['email'],
            username=attrs['username'],
            is_master=attrs['is_master'],
            password=make_password(attrs['password']),
            is_active=True,
        )
        setKey(
            key=attrs['email'],
            value={
                "user": user,
                "activate_code": activate_code
            },
            timeout=1000
        )
        subject = "Activate Your Account"
        html_content = render_to_string('activation.html', {'user': user, 'activate_code': activate_code})
        text_content = strip_tags(html_content)
        print(getKey(key=attrs['email']))

        from_email = f"Aura Team <{settings.EMAIL_HOST_USER}>"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[attrs['email']]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return super().validate(attrs)

        # print(getKey(key=attrs['email']))
        # send_mail(
        #     subject="Subject here",
        #     message=f"Your activate code.\n{activate_code}",
        #     from_email=EMAIL_HOST_USER,
        #     recipient_list=[attrs['email']],
        #     fail_silently=False,
        # )
        # return super().validate(attrs)


class CheckActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            return attrs
        print(data)
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    # services = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'username', 'bio', 'gender', 'telegram', 'instagram', 'facebook',
                  'address', 'image', 'is_master', 'card_num', 'card_exp', 'card_cvv']

    # def get_services(self, user):
    #     services = user.services.all()
    #     serializer = ServiceModelSerializer(services, many=True)
    #     return serializer.data


class UserModelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ('id', 'phone', 'gender', 'address')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        request_user = self.context['request'].user
        user = request_user
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.address = address
        user.save()
        return user


class UserServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'username', 'image']


class BalanceSerializer(serializers.ModelSerializer):
    card_num = serializers.IntegerField(max_value=9999999999999999)
    card_exp = serializers.DateField()
    card_cvv = serializers.IntegerField(max_value=999)

    class Meta:
        model = User
        fields = ('id', 'card_num', 'card_exp', 'card_cvv')

    def update(self, instance, validated_data):
        instance.card_num = validated_data.get('card_num', instance.card_num)
        instance.card_exp = validated_data.get('card_exp', instance.card_exp)
        instance.card_cvv = validated_data.get('card_cvv', instance.card_cvv)
        instance.save()
        return instance


from rest_framework import serializers

class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        verification_code = self.generate_verification_code()

        # Save the activation code to the cache
        cache.set(email, verification_code, timeout=600)  # Cache for 10 minutes

        html_content = render_to_string('activation_payment.html',
                                        {'activate_code': verification_code, 'user': {'full_name': 'User'}})
        text_content = strip_tags(html_content)

        subject = 'Your Verification Code'
        from_email = 'from@example.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return validated_data

    def generate_verification_code(self):
        return str(random.randint(100000, 999999))


class CheckActivationCodePaySerializer(serializers.Serializer):
    import json

    class CheckActivationCodePaySerializer(serializers.Serializer):
        email = serializers.EmailField()
        activate_code = serializers.CharField(max_length=6)

        def validate(self, attrs):
            data = getKey(key=attrs['email'])
            if data:
                data = json.loads(data)  # Parse the JSON string into a dictionary
                if data['activate_code'] == attrs['activate_code']:
                    return attrs
            raise serializers.ValidationError(
                {"error": "Error activate code or email"}
            )
