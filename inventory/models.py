from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, date

# Create your models here.


class Drug(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    wholesale_price = models.DecimalField(decimal_places=2, max_digits=10)
    retail_price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory = models.PositiveBigIntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def default_expiry():
        return date.today() + timedelta(days=500) 
    
    expiry_date = models.DateField(default=default_expiry)

    def is_expired(self):
        return self.expiry_date < date.today()
    
    def is_expiring_soon(self, days=30):
        return date.today() <= self.expiry_date <= date.today() + timedelta(days=days)
    
    def __str__(self):
        desc = self.description[:50] if self.description else ""
        return f"{self.name} {desc}"
    
    def clean(self):
        if self.wholesale_price >= self.retail_price:
            raise ValidationError('Retail price must be higher than wholesale price.')


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_in_stock(self, quantity):
        return self.inventory >=  quantity


    def make_wholesale_sale(self, quantity):
        if not self.is_in_stock(quantity):
            raise ValidationError('Drug is low in stock')
        self.inventory -= quantity
        total_cost = quantity * self.wholesale_price
        self.save()
        return total_cost

    def make_retail_sale(self, quantity):
        if not self.is_in_stock(quantity):
            raise ValidationError('Drug is low in stock')
        self.inventory -= quantity
        total_cost = quantity * self.retail_price
        self.save()
        return total_cost

    def restock(self, quantity):
        if quantity <= 0:
            raise ValidationError('Invalid amount')
        self.inventory += quantity
        self.save()