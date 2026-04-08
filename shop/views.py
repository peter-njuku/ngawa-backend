from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryViewSet(viewsets.ModelViewSet):
    """API ViewSet for Categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    search_fields = ['name']
    ordering_fields = ['name']

class ProductViewSet(viewsets.ModelViewSet):
    """API ViewSet for Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        
        if category:
            if category.lower() == 'all':
                return queryset
            queryset = queryset.filter(category__slug=category)
        
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        products = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
