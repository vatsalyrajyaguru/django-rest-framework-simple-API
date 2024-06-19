from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    email = models.EmailField(unique=True)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Change related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Change related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Address(models.Model):
    address = models.CharField(max_length=124)
    landmark = models.CharField(max_length=64, null=True, blank=True)
    pincode = models.CharField(max_length=6)
    post_office = models.CharField(max_length=64, null=True, blank=True)
    district = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)

class Customer(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female')
    ]
    full_name = models.CharField(max_length=32)
    mobile_number = models.CharField(max_length=10)
    birthdate = models.DateField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    addresses = models.ManyToManyField(Address)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

