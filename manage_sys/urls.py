from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from manage_sys import views
from .views import UserViewSet, CompanyViewSet, ProfileViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

company_list = CompanyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
company_detail = CompanyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

profile_cr = ProfileViewSet.as_view({
    'post': 'create',
})
profile_ds = ProfileViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('users/',
        user_list,
        name='user-list'),
    path('users/<int:pk>',
        user_detail,
        name='user-detail'),
    path('companies/',
        company_list,
        name='companies-list'),
    path('companies/<int:pk>',
        company_detail,
        name='company-detail'),
    path('profile/',
        profile_cr,
        name='profile-list'),
    path('profile/<int:pk>',
        profile_ds,
        name='profile-detail'),
])