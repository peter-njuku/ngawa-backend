"""
Management command to seed default product categories.
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Seed default product categories'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Desktops',
                'description': 'Desktop computers and systems'
            },
            {
                'name': 'Laptops',
                'description': 'Laptop computers and portable devices'
            },
            {
                'name': 'Printers',
                'description': 'Printers and printing devices'
            },
            {
                'name': 'Accessories',
                'description': 'Computer accessories and peripherals'
            },
        ]

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded all categories!')
        )
