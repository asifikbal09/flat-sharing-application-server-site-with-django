from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            'user': request.user.id,
            'flat': request.data.get('flatId'),
            'status': 'PENDING'
        }
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'statusCode': 201,
                'message': 'Booking requests submitted successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Booking failed',
            'errorDetails': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response({
            'success': True,
            'statusCode': 200,
            'message': 'Booking requests retrieved successfully',
            'data': serializer.data
        })


class BookingUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'statusCode': 200,
                'message': 'Booking request updated successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'Update failed',
            'errorDetails': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)