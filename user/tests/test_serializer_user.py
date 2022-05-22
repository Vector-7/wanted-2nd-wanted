from rest_framework import serializers
from rest_framework.test import APITestCase

from user.serializers import UserSerializer


class SerializerUserTest(APITestCase):

    def test_failed_nickname(self):
        """
        nickname은 4자 이상 32자 이하이다.
        """
        req = {
            'nickname': 'abc',
            'password': 'aaaakkkkbbbccc',
            'level': 'client',
            'email': 'seokbong651@gmail.com',
        }
        s = UserSerializer(data=req)
        self.assertRaises(serializers.ValidationError, s.is_valid,
                          **{'raise_exception': True})

        req = {
            'nickname': 'a' * 33,
            'password': 'aaaakkkkbbbccc',
            'level': 'client',
            'email': 'seokbong651@gmail.com',
        }
        s = UserSerializer(data=req)
        self.assertRaises(serializers.ValidationError, s.is_valid,
                          **{'raise_exception': True})

    def test_failed_level(self):
        """
        level은 다른게 들어와선 안된다.
        """
        req = {
            'nickname': 'rams',
            'password': 'aaaakkkkbbbccc',
            'level': 'clients',
            'email': 'seokbong651@gmail.com',
        }
        s = UserSerializer(data=req)
        self.assertRaises(serializers.ValidationError, s.is_valid,
                          **{'raise_exception': True})
