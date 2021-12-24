from collections import OrderedDict
import json
from django.shortcuts import get_object_or_404
from rest_framework import response, serializers
from rest_framework.fields import ChoiceField, SerializerMethodField
from rest_framework.request import Request
from .models import User, Company, Profile
from django.contrib.auth.models import User as U
from django.core import serializers as s
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField( 
           min_length=6, 
           max_length=68, 
           write_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class CompanySerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=100)
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        profile = Profile.objects.filter(company_id=obj.id)
        if profile:
            a = list()
            serializer = ProfileSerializer(profile, many=True)
            for i in range(len(serializer.data)):
                user = User.objects.get(id=serializer.data[i]['user'])
                a.append(user)
            serU = UserSerializer(a, many=True)
            return serU.data

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     users = Profile.objects.filter(user=validated_data['user'])
    #     if users:
    #         raise serializers.ValidationError({"detail": "user exists!"})
    #     return Company.objects.create(**validated_data)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'company']


