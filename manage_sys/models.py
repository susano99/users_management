from django.db import models
from django.contrib.auth.models import User as U
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

class User(U):
    
    phone = models.CharField(max_length=11)

    # def __str__(self):
    #     return f'{self.username}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'{self.user.username} and {self.company}'
