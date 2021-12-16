from rest_framework import serializers
from .models import User, Company, Profile
# from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.CharField(source='user.username')
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'phone', 'password']


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ['url', 'id', 'name', 'country', 'city', 'phone']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ['url', 'id', 'users', 'company']