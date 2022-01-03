from django.shortcuts import get_object_or_404, render
from .models import User, Company, Profile
from .serializers import CompanySerializer, ProfileSerializer
from rest_framework import generics, renderers, viewsets, permissions, mixins
from rest_framework import response, serializers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect
from rest_framework import status


class UserViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class UserCreateSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=100)
        email = serializers.EmailField()
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        phone = serializers.CharField(max_length=100)
        password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            )
    
    class UserUpdateSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=100)
        email = serializers.EmailField()
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        phone = serializers.CharField(max_length=100)

    class UserPassChangeSerializer(serializers.Serializer):
        password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            write_only=True)
        new_password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            write_only=True)
        
    class UserPassResetSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            write_only=True)

    class BriefInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == "perform_create":
            return self.UserCreateSerializer
        if self.action == "get_list":
            return self.BriefInfoSerializer
        if self.action == "perform_update":
            return self.UserUpdateSerializer
        if self.action == "change_password":
            return self.UserPassChangeSerializer
        if self.action == "reset_password":
            return self.UserPassResetSerializer
        return self.UserCreateSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)
    
    @action(methods=['post'], detail=True)
    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(**serializer.data)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(methods=['patch'], detail=True)
    def perform_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.username = serializer.validated_data.get("username", user.username)
        user.email = serializer.validated_data.get("email", user.email)
        user.first_name = serializer.validated_data.get("first_name", user.first_name)
        user.last_name = serializer.validated_data.get("last_name", user.last_name)
        user.phone = serializer.validated_data.get("phone", user.phone)
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_list(self, request, *args, **kwargs):
        people = User.objects.all()
        data = self.get_serializer(people, many=True).data
        return Response(data)

    @action(methods=['patch'],
            detail=True,
            url_name='change-password',
            url_path='change-password'
            )
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_pass = serializer.validated_data.get("password")
        if user.password == old_pass:
            new_pass = serializer.validated_data.get("new_password")
            if new_pass:
                user.password = new_pass
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError({"detail": "type new password!"})
        raise serializers.ValidationError({"detail": "wrong old password!"})
    
    @action(methods=['patch'],
            detail=True,
            url_name='reset-password',
            url_path='reset-password'
            )
    def reset_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        if user.email == email:
            new_pass = serializer.validated_data.get("password")
            if new_pass:
                user.password = new_pass
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError({"detail": "type new password!"})
        raise serializers.ValidationError({"detail": "wrong email!"})

    @action(methods=['patch'],
            detail=True,
            url_name='account',
            url_path='account')
    def activate_deactivate_account(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        if username[0] != "!":
            user.username = f'!{user.username}'
            user.save()
            return Response(status=status.HTTP_200_OK)
        elif username[0] == "!":
            user.username = user.username[1:]
            user.save()
            return Response(status=status.HTTP_200_OK)


class CompanyViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    

class ProfileViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'companies': reverse('companies-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
    })