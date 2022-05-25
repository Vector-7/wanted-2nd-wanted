from rest_framework import serializers

from company.models import CompanyName, CompanyTagItem


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CompanyName


class CompanyTagItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CompanyTagItem
