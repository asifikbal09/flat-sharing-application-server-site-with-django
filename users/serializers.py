from rest_framework import serializers
from .models import User
from profiles.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(write_only=True, required=False)
    profession = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'bio', 'profession', 'address']

    def create(self, validated_data):
        bio = validated_data.pop('bio', None)
        profession = validated_data.pop('profession', None)
        address = validated_data.pop('address', None)

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        UserProfile.objects.create(
            user=user,
            bio=bio,
            profession=profession,
            address=address
        )

        return user