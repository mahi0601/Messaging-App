# messaging/management/commands/create_default_user.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a default user if not already created'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="default_user").exists():
            User.objects.create_user(
                username="user",
                password="1234",
                email="user@example.com"
            )
            self.stdout.write(self.style.SUCCESS("Default user created"))
        else:
            self.stdout.write(self.style.WARNING("User already exists"))
