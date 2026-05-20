from django.core.management.base import BaseCommand
from inventory.models import Drug
from sales.models import Sale, SaleItem

class Command(BaseCommand):
    help = 'Wipe DB of items'

    def handle(self, *args, **options):
        SaleItem.objects.all().delete()
        Sale.objects.all().delete()
        deleted_count, _ = Drug.objects.all().delete()
        self.stdout.write(f'Successfully deleted {deleted_count} items')