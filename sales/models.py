from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
User = get_user_model()
from inventory.models import Drug
from accounts.models import Customer

# Create your models here.


class Sale(models.Model):
    class SaleType(models.TextChoices):
        WHOLESALE = 'WHOLESALE', 'Wholesale'
        RETAIL = 'RETAIL', 'Retail'
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    type = models.CharField(max_length=50, choices=SaleType.choices)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale by {self.seller}"

    


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def unit_price(self):
        if self.quantity > 0:
            return self.total_cost / self.quantity
        return 0

    def save(self,*args, **kwargs):
        if not self.pk:
            if self.sale.type == self.sale.SaleType.WHOLESALE:
                self.total_cost = self.drug.make_wholesale_sale(self.quantity)
            elif self.sale.type == self.sale.SaleType.RETAIL:
                self.total_cost = self.drug.make_retail_sale(self.quantity)

        super().save(*args, **kwargs)
        self.sale.total_cost = self.sale.saleitem_set.aggregate(
            total=Sum('total_cost')
        )['total']
        self.sale.save(update_fields=['total_cost'])

