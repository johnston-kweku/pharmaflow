from django.core.management.base import BaseCommand
from inventory.models import Drug
import json



class Command(BaseCommand):
    help = 'Load drugs from JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the JSON file')
    
    def handle(self, *args, **options):
        file_path = options['file']

        if not file_path:
            self.stderr.write('Please provide a file path using --file')
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        count = 0
        for item in data:
            Drug.objects.create(
                name=item['name'],
                description=item['description'],
                wholesale_price=item['wholesale_price'],
                retail_price=item['retail_price'],
                inventory=item['inventory'],
                cost_price=item['cost_price']
            )
            count += 1

        self.stdout.write(f'Successfully loaded {count} items')