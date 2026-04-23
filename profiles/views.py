from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response({
                'success': True,
                'statusCode': 200,
                'message': 'User profile retrieved successfully',
                'data': serializer.data
            })
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'statusCode': 200,
                'message': 'User profile updated successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'Update failed',
            'errorDetails': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)