from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import CharField, TextField, DateField, DateTimeField, PositiveBigIntegerField, DecimalField
from faker import Faker
from datetime import timedelta, date
from random_word import RandomWords
import random


class Command(BaseCommand):
    help = 'Edit a field with random data'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str, help='app_label.ModelName eg. inventory.Drug')
        parser.add_argument('--field', type=str, help='Field name to populate')

    def handle(self, *args, **options):
        model_path = options['model']
        field_name = options['field']

        app_label, model_name = model_path.split('.')
        model = apps.get_model(app_label, model_name)
        field = model._meta.get_field(field_name)
        r = RandomWords()
        fake = Faker()
        
        updated = 0
        for instance in model.objects.all():
            if isinstance(field, CharField):
                data = r.get_random_word()
            elif isinstance(field, TextField):
                data = fake.paragraph(nb_sentences=6)
            elif isinstance(field, DateField):
                margin = random.randint(-500, 500)
                data = date.today() + timedelta(days=margin)
            elif isinstance(field, DecimalField):
                data = random.randint(-100, 100)
            elif isinstance(field, PositiveBigIntegerField):
                data = random.randint(50, 1000)
            setattr(instance, field_name, data)
            instance.save()
            updated +=1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated} records.'))


