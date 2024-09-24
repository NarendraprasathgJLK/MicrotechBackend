from django.core.management.base import BaseCommand
from tracking.models import SerialNumber

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        SerialNumber.objects.get_or_create(serial_number='sc001')
        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))
