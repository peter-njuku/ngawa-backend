# serializers.py
from rest_framework import serializers
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    # Write-only field that accepts the uploaded file
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'category', 'category_name',
            'stock', 'is_active',
            'image',      # write-only: accepts file upload
            'image_url',  # read-only: returns Cloudinary URL
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image:  # CloudinaryField falsy when empty
            return obj.image.url
        return None

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        product = Product(**validated_data)
        if image:
            product.image = image  # django-cloudinary-storage handles the upload
        product.save()
        return product

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if image:
            instance.image = image
        instance.save()
        return instance