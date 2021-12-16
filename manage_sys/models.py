from django.db import models
from django.contrib.auth.models import User as U
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

class User(U):
    # user = models.OneToOneField(U, related_name='user', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.username}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    users = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.users.username} and {self.company}'
