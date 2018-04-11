from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.fields import ImageField
from rest_framework.validators import UniqueValidator

User = get_user_model()

__all__ = (
    'UserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    password = serializers.CharField(min_length=5, write_only=True)
    img_profile = serializers.ImageField(default='')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            email=validated_data['username'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            img_profile=validated_data['img_profile'],
        )
        return user

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'img_profile',
        ]
