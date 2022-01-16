from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):          
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):          
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):          
        return self.name

class Item(models.Model):
    document_date = models.DateField()
    balance = models.IntegerField()
    supplier = models.ForeignKey(Supplier, related_name='supplier', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, related_name='currency', on_delete=models.CASCADE)


