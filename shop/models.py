from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    """Product Categories"""
    CATEGORY_CHOICES = [
        ('laptops', 'Laptops'),
        ('desktops', 'Desktops'),
        ('printers', 'Printers'),
        ('accessories', 'Accessories'),
        ('networking', 'Networking'),
        ('repairs', 'Repair Services'),
        ('ewaste', 'E-Waste Dumping'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Products and Services"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image_url = models.URLField(blank=True, null=True, help_text="Vercel Blob URL for product image")
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
        ]
    
    def __str__(self):
        return self.name
