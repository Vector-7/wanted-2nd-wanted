from rest_framework import serializers
from rest_framework.test import APITestCase

from user.utils.queries import UserQuery


class SerializerUserTest(APITestCase):

    def test_failed_nickname(self):
        """
        nickname은 4자 이상 32자 이하이다.
        """

        with self.assertRaises(serializers.ValidationError):
            UserQuery().create(nickname='abc',
                               password='aaaakkkkbbbccc',
                               level='client',
                               email='seokbong60@gmail.com')

        with self.assertRaises(serializers.ValidationError):
            UserQuery().create(nickname='a' * 33,
                               password='aaaakkkkbbbccc',
                               level='client',
                               email='seokbong60@gmail.com')

    def test_failed_level(self):
        """
        level은 다른게 들어와선 안된다.
        """

        with self.assertRaises(serializers.ValidationError):
            UserQuery().create(nickname='a' * 33,
                               password='aaaakkkkbbbccc',
                               level='clients',
                               email='seokbong60@gmail.com')
