"""
Views for products and categories REST API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model.
    GET: All users can list and retrieve categories.
    POST, PUT, DELETE: Admin users only.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Set permissions based on action.
        Read actions: Anyone can access
        Write actions: Admin only
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in a category."""
        category = self.get_object()
        products = category.products.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model.
    GET: All users can list and retrieve products.
    POST, PUT, DELETE: Admin users only.
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get all products, optionally filtered by category."""
        queryset = Product.objects.select_related('category').all()
        category_id = self.request.query_params.get('category_id', None)
        
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def get_permissions(self):
        """
        Set permissions based on action.
        Read actions: Anyone can access
        Write actions: Admin only
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get products grouped by category."""
        categories = Category.objects.all()
        data = {}
        
        for category in categories:
            products = Product.objects.filter(category=category, is_active=True)
            data[category.name] = ProductSerializer(products, many=True).data
        
        return Response(data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active products."""
        products = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
