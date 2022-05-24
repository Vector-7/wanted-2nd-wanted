from rest_framework import serializers

from company.models import CompanyName, CompanyTag


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CompanyName


class CompanyTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CompanyTag
