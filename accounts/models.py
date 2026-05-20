from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class UserRoles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        WHOLESALER = 'WHOLESALER', 'Wholesaler'
        RETAILER = 'RETAILER', 'Retailer'

    full_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=UserRoles.choices,
        null=False,
        blank=False
    )
    phone_number = models.CharField(max_length=15, blank=True, default='')


    def is_admin(self):
        return self.role == self.UserRoles.ADMIN
    
    def is_manager(self):
        return self.role == self.UserRoles.MANAGER
    
    def is_wholesaler(self):
        return self.role == self.UserRoles.WHOLESALER
    
    def is_retailer(self):
        return self.role == self.UserRoles.RETAILER

    def can_create_role(self, role):
        if self.is_admin():
            return role in [
                self.UserRoles.MANAGER,
                self.UserRoles.WHOLESALER,
                self.UserRoles.RETAILER
            ]
        
        if self.is_manager():
            return role in [
                self.UserRoles.WHOLESALER,
                self.UserRoles.RETAILER
            ]
        
        return False
    

class Customer(models.Model):
    name = models.CharField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.phone_number}'