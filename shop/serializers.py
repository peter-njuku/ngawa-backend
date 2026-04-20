from rest_framework import serializers
from .models import Category, Product
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name', 'full_name',
                    'password', 'date_joined', 'is_staff']
        read_only_fields = ['id', 'date_joined']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(validated_data['password'])
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']
        read_only_fields = ['id']

    def get_product_count(self, obj):
        return obj.products.count()
 
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 
            'category_name', 'image', 'in_stock', 'featured', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0: raise serializers.ValidationError("Stock quatity cannot be zero")
        return value
    

class DashboardStatsSerializer(serializers.Serializer):
    total_products  = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_users = serializers.IntegerField()
    low_stock_products = ProductSerializer(many=True)
    