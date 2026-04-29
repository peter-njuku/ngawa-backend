"""
Management command to initialize the default admin user.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create or update the default admin user'

    def handle(self, *args, **options):
        admin_username = 'admin'
        admin_password = 'Admin123.'
        admin_email = 'admin@ngawasolutions.com'

        if User.objects.filter(username=admin_username).exists():
            user = User.objects.get(username=admin_username)
            user.set_password(admin_password)
            user.email = admin_email
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated admin user: {admin_username}')
            )
        else:
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: {admin_username}')
            )

        self.stdout.write(
            self.style.SUCCESS('Admin initialization complete!')
        )
