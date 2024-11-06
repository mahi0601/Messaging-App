import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from messaging.models import Customer, Message
from django.conf import settings

class Command(BaseCommand):
    help = 'Load messages from CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR / 'GeneralistRails_Project_MessageData.csv'
        
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Update these keys based on your actual CSV header
                customer_name = row['User ID']  # Assuming 'User' is the correct column
                message_content = row['Message Body']  # Update as per actual header
                
                customer, _ = Customer.objects.get_or_create(name=customer_name)
                Message.objects.create(customer=customer, content=message_content, urgency='urgent' in message_content.lower())
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded messages'))
