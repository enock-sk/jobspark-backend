from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Job, ContactMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'role']

class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['created_at', 'is_resolved']