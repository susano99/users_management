from django.shortcuts import get_object_or_404, render
from .models import User, Company, Profile
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
            style={'input_type': 'password', 'placeholder': 'password'},
            min_length=6, 
            max_length=68)
    
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
            style={'input_type': 'password', 'placeholder': 'password'},
            write_only=True)
        new_password = serializers.CharField( 
            min_length=6, 
            max_length=68,
            style={'input_type': 'password', 'placeholder': 'password'}, 
            write_only=True)
        retype_new_password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            style={'input_type': 'password', 'placeholder': 'password'},
            write_only=True)
        
    class UserPassResetSerializer(serializers.Serializer):
        email = serializers.EmailField()

    class UserPassConfirmSerializer(serializers.Serializer):
        token = serializers.CharField(max_length=100)
        new_password = serializers.CharField( 
            min_length=6, 
            max_length=68,
            style={'input_type': 'password', 'placeholder': 'password'}, 
            write_only=True)
        retype_new_password = serializers.CharField( 
            min_length=6, 
            max_length=68, 
            style={'input_type': 'password', 'placeholder': 'password'},
            write_only=True)

    class BriefInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == "create":
            return self.UserCreateSerializer
        if self.action == "list":
            return self.BriefInfoSerializer
        if self.action == "update":
            return self.UserUpdateSerializer
        if self.action == "retrieve":
            return self.UserUpdateSerializer
        if self.action == "change_password":
            return self.UserPassChangeSerializer
        if self.action == "reset_password":
            return self.UserPassResetSerializer
        if self.action == "confirm_password":
            return self.UserPassConfirmSerializer
        return self.UserCreateSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        User.objects.create(
            username = serializer.validated_data.get("username"),
            email = serializer.validated_data.get("email"),
            first_name = serializer.validated_data.get("first_name"),
            last_name = serializer.validated_data.get("last_name"),
            phone = serializer.validated_data.get("phone"),
            password = serializer.validated_data.get("password"),
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.username = serializer.validated_data.get('username')
        user.email = serializer.validated_data.get('email')
        user.first_name = serializer.validated_data.get('first_name')
        user.last_name = serializer.validated_data.get('last_name')
        user.phone = serializer.validated_data.get('phone')
        user.save()

    def perform_destroy(self, instance):
        instance.delete()

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
                new_pass1 = serializer.validated_data.get("retype_new_password")
                if new_pass == new_pass1:
                    user.password = new_pass
                    user.save()
                    return Response({"Success": "Password Changed!"}, status=status.HTTP_200_OK)
                else:
                    raise serializers.ValidationError({"detail": "passwords do not match!"})
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
            url = f'http://127.0.0.1:8000/users/{user.id}/confirm-password'
            return HttpResponseRedirect(redirect_to=url)
        raise serializers.ValidationError({"detail": "wrong email!"})

    @action(methods=['patch'],
            detail=True,
            url_name='confirm-password',
            url_path='confirm-password'
            )
    def confirm_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token1 = '5CbvCwyp0XKsw6r98fXF871cydVBiam8'
        token = serializer.validated_data.get("token")
        if token == token1:
            new_pass = serializer.validated_data.get("new_password")
            if new_pass:
                new_pass_con = serializer.validated_data.get("retype_new_password")
                if new_pass == new_pass_con:
                    user.password = new_pass
                    user.save()
                    return Response({"Success": "Password Changed!"}, status=status.HTTP_200_OK)
                else:
                    raise serializers.ValidationError({"detail": "passwords don't match!"})
            else:
                raise serializers.ValidationError({"detail": "type new password!"})
        else:
            raise serializers.ValidationError({"detail": "wrong token!"})

    @action(methods=['patch'],
            detail=True,
            url_name='account',
            url_path='account')
    def activate_deactivate_account(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return Response(status=status.HTTP_200_OK)

class CompanyViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class CompanyCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        country = serializers.CharField(max_length=100)
        city = serializers.CharField(max_length=100)
        phone = serializers.CharField(max_length=100)

    class BriefInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Company
            fields = ['id', 'name', 'country', 'city']

    class CompanyRetrieveSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        country = serializers.CharField(max_length=100)
        city = serializers.CharField(max_length=100)
        phone = serializers.CharField(max_length=100)
        users = serializers.SerializerMethodField()

        def get_users(self, obj):
            a = Company.objects.get(id=obj.id)
            b = a.users.all()
            serU = UserViewSet().BriefInfoSerializer(b, many=True)
            return serU.data

    def get_serializer_class(self):
        if self.action == "create":
            return self.CompanyCreateSerializer
        if self.action == "list":
            return self.BriefInfoSerializer
        if self.action == "retrieve":
            return self.CompanyRetrieveSerializer
        return self.CompanyCreateSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Company.objects.create(
            name = serializer.validated_data.get("name"),
            country = serializer.validated_data.get("country"),
            city = serializer.validated_data.get("city"),
            phone = serializer.validated_data.get("phone"),
        )
    

class ProfileViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class ProfileSerializer(serializers.ModelSerializer):

        class Meta:
            model = Profile
            fields = ['id', 'user', 'company']

    def get_serializer_class(self):
        if self.action == "create":
            return self.ProfileSerializer
        if self.action == "delete":
            return self.ProfileSerializer
        return self.ProfileSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'companies': reverse('companies-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
    })