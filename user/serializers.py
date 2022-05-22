from rest_framework import serializers

from core.miniframework_on_django.tools.password import hash_password
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    level = serializers.CharField(max_length=20)

    def validate_level(self, level):
        if level not in User.USER_LEVEL_MAP:
            # client/company_client/admin 중 하나 여야 한다.
            raise serializers.ValidationError('level matching failed')
        return User.USER_LEVEL_MAP[level]

    def validate_nickname(self, nickname):
        if not (3 < len(nickname) < 33):
            raise serializers.ValidationError('nickname matching failed')

    def create(self, validated_data):
        # password 암호화
        validated_data['password'] = hash_password(validated_data['password'])
        # Save data
        user = User(**validated_data)
        user.save()

        return user

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password', 'level')
