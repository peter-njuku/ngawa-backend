"""
Script to initialize sample products and categories for Ngawa Solutions
Run this after migrations: python manage.py shell < scripts/init_sample_data.py
"""

from shop.models import Category, Product
from decimal import Decimal

# Clear existing data (optional - comment out to keep existing data)
# Category.objects.all().delete()
# Product.objects.all().delete()

# Create categories
categories_data = [
    {'name': 'Laptops', 'slug': 'laptops', 'description': 'Portable computers for business and personal use'},
    {'name': 'Desktops', 'slug': 'desktops', 'description': 'High-performance desktop computers'},
    {'name': 'Printers', 'slug': 'printers', 'description': 'Printers and multifunction devices'},
    {'name': 'Accessories', 'slug': 'accessories', 'description': 'Computer accessories and peripherals'},
    {'name': 'Networking', 'slug': 'networking', 'description': 'Networking equipment and devices'},
    {'name': 'Repair Services', 'slug': 'repairs', 'description': 'Professional repair and maintenance services'},
    {'name': 'E-Waste Dumping', 'slug': 'ewaste', 'description': 'Responsible e-waste management and recycling'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
        }
    )
    categories[cat.slug] = cat
    print(f"{'Created' if created else 'Exists'}: {cat.name}")

# Create sample products
products_data = [
    # Laptops
    {
        'name': 'Dell XPS 13 Laptop',
        'description': 'Ultra-portable laptop with Intel Core i7, 16GB RAM, 512GB SSD. Perfect for professionals.',
        'price': Decimal('1299.99'),
        'category': 'laptops',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'HP ProBook 450 G9',
        'description': 'Business laptop with 15.6" display, Intel Core i5, 8GB RAM. Great for business users.',
        'price': Decimal('899.99'),
        'category': 'laptops',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'Lenovo ThinkPad E15',
        'description': 'Reliable business laptop with excellent keyboard and performance.',
        'price': Decimal('799.99'),
        'category': 'laptops',
        'in_stock': True,
        'featured': False,
    },
    
    # Desktops
    {
        'name': 'Dell Optiplex 7090',
        'description': 'Professional desktop with Intel Core i7, 16GB RAM, 256GB SSD. Ideal for offices.',
        'price': Decimal('1199.99'),
        'category': 'desktops',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'HP EliteDesk 800 G6',
        'description': 'Compact desktop for business environments with excellent performance.',
        'price': Decimal('1099.99'),
        'category': 'desktops',
        'in_stock': True,
        'featured': False,
    },
    
    # Printers
    {
        'name': 'HP LaserJet Pro M404n',
        'description': 'Professional black & white laser printer. Print speed: 40 ppm. Network ready.',
        'price': Decimal('449.99'),
        'category': 'printers',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'Canon imageCLASS MF445dw',
        'description': 'Multifunction printer with copy, scan, and fax. Wireless connectivity.',
        'price': Decimal('699.99'),
        'category': 'printers',
        'in_stock': True,
        'featured': False,
    },
    
    # Accessories
    {
        'name': 'Logitech Wireless Mouse',
        'description': 'Reliable wireless mouse with 2.4GHz connection. Long battery life.',
        'price': Decimal('29.99'),
        'category': 'accessories',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'Dell Mechanical Keyboard',
        'description': 'Professional mechanical keyboard with RGB backlight. USB connection.',
        'price': Decimal('149.99'),
        'category': 'accessories',
        'in_stock': True,
        'featured': False,
    },
    
    # Networking
    {
        'name': 'Cisco Catalyst 2960X Switch',
        'description': 'Managed switch with 48 Gigabit Ethernet ports. For enterprise networks.',
        'price': Decimal('2499.99'),
        'category': 'networking',
        'in_stock': True,
        'featured': False,
    },
    {
        'name': 'TP-Link WiFi 6 Router',
        'description': 'High-speed WiFi 6 router with MU-MIMO technology. Range: 2500 sq ft.',
        'price': Decimal('199.99'),
        'category': 'networking',
        'in_stock': True,
        'featured': True,
    },
    
    # Services
    {
        'name': 'Computer Repair Service',
        'description': 'Professional computer repair, diagnostics, and hardware replacement. $50/hour.',
        'price': Decimal('50.00'),
        'category': 'repairs',
        'in_stock': True,
        'featured': True,
    },
    {
        'name': 'Network Setup Service',
        'description': 'Complete network setup, configuration, and testing for small to medium businesses.',
        'price': Decimal('300.00'),
        'category': 'networking',
        'in_stock': True,
        'featured': False,
    },
    {
        'name': 'E-Waste Recycling Service',
        'description': 'Responsible disposal and recycling of old computers and electronic equipment.',
        'price': Decimal('0.00'),
        'category': 'ewaste',
        'in_stock': True,
        'featured': True,
    },
]

for prod_data in products_data:
    category = categories[prod_data.pop('category')]
    
    prod, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'category': category,
            **prod_data
        }
    )
    print(f"{'Created' if created else 'Exists'}: {prod.name} - ${prod.price}")

print("\n✓ Sample data initialization complete!")
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
