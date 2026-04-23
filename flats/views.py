from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Flat
from .serializers import FlatSerializer

class FlatListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get(self, request):
        queryset = Flat.objects.all()
        
        # Search
        search_term = request.query_params.get('searchTerm')
        if search_term:
            queryset = queryset.filter(
                Q(location__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(utilities_description__icontains=search_term)
            )

        # Filtering
        availability = request.query_params.get('availability')
        if availability:
            queryset = queryset.filter(availability=availability)

        # Sorting
        sort_by = request.query_params.get('sortBy')
        sort_order = request.query_params.get('sortOrder', 'asc')
        if sort_by:
            if sort_order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)

        # Pagination
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        start = (page - 1) * limit
        end = start + limit
        total = queryset.count()

        serializer = FlatSerializer(queryset[start:end], many=True)
        return Response({
            'success': True,
            'statusCode': 200,
            'message': 'Flats retrieved successfully',
            'meta': {'total': total, 'page': page, 'limit': limit},
            'data': serializer.data
        })

    def post(self, request):
        serializer = FlatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'statusCode': 201,
                'message': 'Flat added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to add flat',
            'errorDetails': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class FlatUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, flat_id):
        try:
            flat = Flat.objects.get(id=flat_id)
        except Flat.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Flat not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FlatSerializer(flat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'statusCode': 200,
                'message': 'Flat information updated successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'Update failed',
            'errorDetails': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)