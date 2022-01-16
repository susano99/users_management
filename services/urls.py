from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from services import views
from .views import CompanyViewSet, SupplierViewSet, CurrencyViewSet, ItemViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


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

supplier_list = SupplierViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
supplier_detail = SupplierViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

currency_list = CurrencyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
currency_detail = CurrencyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

item_list = ItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
item_detail = ItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

item_filterS = ItemViewSet.as_view({
    'get': 'filter_supplier',
})
item_filterC = ItemViewSet.as_view({
    'get': 'filter_company',
})
item_filterCU = ItemViewSet.as_view({
    'get': 'filter_currency',
})

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('company/',
        company_list,
        name='company-list'),
    path('company/<int:pk>',
        company_detail,
        name='company-detail'),
    path('suppliers/',
        supplier_list,
        name='supplier-list'),
    path('suppliers/<int:pk>',
        supplier_detail,
        name='supplier-detail'),
    path('currency/',
        currency_list,
        name='currency-list'),
    path('currency/<int:pk>',
        currency_detail,
        name='currency-detail'),
    path('item/',
        item_list,
        name='item-list'),
    path('item/<int:pk>',
        item_detail,
        name='item-detail'),
    path('item/<int:supplierid>/supplier',
        item_filterS,
        name='filter-supplier'),
    path('item/<int:companyid>/company',
        item_filterC,
        name='filter-company'),
    path('item/<int:currencyid>/currency',
        item_filterCU,
        name='filter-currency'),
])