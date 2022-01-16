from django.shortcuts import get_object_or_404, render
from .models import Supplier, Company, Currency, Item
from rest_framework import generics, renderers, viewsets, permissions, mixins
from rest_framework import response, serializers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponseRedirect
from rest_framework import status



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

    def get_serializer_class(self):
        if self.action == "create":
            return self.CompanyCreateSerializer
        if self.action == "update":
            return self.CompanyCreateSerializer
        if self.action == "list":
            return self.CompanyCreateSerializer
        if self.action == "retrieve":
            return self.CompanyCreateSerializer
        return self.CompanyCreateSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Company.objects.create(
            name = serializer.validated_data.get("name"),
            country = serializer.validated_data.get("country"),
        )
    
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        company = self.get_object()
        company.name = serializer.validated_data.get('name')
        company.country = serializer.validated_data.get('country')
        company.save()

    def perform_destroy(self, instance):
        instance.destroy()

class SupplierViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    
    queryset = Supplier.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class SupplierCreateSerializer(serializers.PrimaryKeyRelatedField, serializers.Serializer):
        name = serializers.CharField(max_length=100)
        phone = serializers.IntegerField()


    def get_serializer_class(self):
        if self.action == "create":
            return self.SupplierCreateSerializer
        if self.action == "update":
            return self.SupplierCreateSerializer
        if self.action == "list":
            return self.SupplierCreateSerializer
        if self.action == "retrieve":
            return self.SupplierCreateSerializer
        return self.SupplierCreateSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Supplier.objects.create(
            name = serializer.validated_data.get("name"),
            phone = serializer.validated_data.get("phone"),
        )
    
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        supplier = self.get_object()
        supplier.name = serializer.validated_data.get('name')
        supplier.phone = serializer.validated_data.get('phone')
        supplier.save()

    def perform_destroy(self, instance):
        instance.destroy()

class CurrencyViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    
    queryset = Currency.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class CurrencyCreateSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)

    def get_serializer_class(self):
        if self.action == "create":
            return self.CurrencyCreateSerializer
        if self.action == "update":
            return self.CurrencyCreateSerializer
        if self.action == "list":
            return self.CurrencyCreateSerializer
        if self.action == "retrieve":
            return self.CurrencyCreateSerializer
        return self.CurrencyCreateSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Currency.objects.create(
            name = serializer.validated_data.get("name"),
        )
    
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        currency = self.get_object()
        currency.name = serializer.validated_data.get('name')
        currency.save()

    def perform_destroy(self, instance):
        instance.destroy()


class ItemViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class ItemCreateSerializer(serializers.ModelSerializer):

        class Meta:
            model = Item
            fields = ['document_date', 'balance', 'supplier', 'company', 'currency']
    
    def get_serializer_class(self):
        if self.action == "create":
            return self.ItemCreateSerializer
        if self.action == "update":
            return self.ItemCreateSerializer
        if self.action == "list":
            return self.ItemCreateSerializer
        if self.action == "filter_supplier":
            return self.ItemCreateSerializer
        if self.action == "filter_company":
            return self.ItemCreateSerializer
        if self.action == "filter_currency":
            return self.ItemCreateSerializer
        return self.ItemCreateSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Item.objects.create(
            document_date = serializer.validated_data.get("document_date"),
            balance = serializer.validated_data.get("balance"),
            supplier = serializer.validated_data.get("supplier"),
            company = serializer.validated_data.get("company"),
            currency = serializer.validated_data.get("currency"),
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        item = self.get_object()
        item.document_date = serializer.validated_data.get('document_date')
        item.balance = serializer.validated_data.get('balance')
        item.supplier = serializer.validated_data.get('supplier')
        item.company = serializer.validated_data.get('company')
        item.currency = serializer.validated_data.get('currency')
        item.save()

    def perform_destroy(self, instance):
        instance.destroy()

    @action(methods=['get'],
            detail=True,
            url_name='filter-supplier',
            url_path='filter-supplier'
            )
    def filter_supplier(self, request, *args, **kwargs):
        queryset = Item.objects.all()
        if self.kwargs['supplierid']:
            filtered = self.ItemCreateSerializer(queryset.filter(supplier=self.kwargs['supplierid']), many=True)
            return Response(filtered.data)

    @action(methods=['get'],
            detail=True,
            url_name='filter-company',
            url_path='filter-company'
            )
    def filter_company(self, request, *args, **kwargs):
        queryset = Item.objects.all()
        if self.kwargs['companyid']:
            filtered = self.ItemCreateSerializer(queryset.filter(company=self.kwargs['companyid']), many=True)
            return Response(filtered.data)

    @action(methods=['get'],
            detail=True,
            url_name='filter-currency',
            url_path='filter-currency'
            )
    def filter_currency(self, request, *args, **kwargs):
        queryset = Item.objects.all()
        if self.kwargs['currencyid']:
            filtered = self.ItemCreateSerializer(queryset.filter(currency=self.kwargs['currencyid']), many=True)
            return Response(filtered.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'company': reverse('company-list', request=request, format=format),
        'suppliers': reverse('supplier-list', request=request, format=format),
        'currency': reverse('currency-list', request=request, format=format),
        'item': reverse('item-list', request=request, format=format),
    })