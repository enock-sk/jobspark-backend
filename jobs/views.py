from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import Job, UserProfile, ContactMessage
from .serializers import JobSerializer, UserProfileSerializer, ContactMessageSerializer

class JobList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        job_type = request.query_params.get('job_type', None)
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

class JobCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'Employer':
            return Response({'error': 'Only Employers can post jobs'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Job posted successfully', 'job': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'JobSeeker'})
            token = AuthToken.objects.create(user)[1]
            return Response({
                'token': token,
                'role': profile.role,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'JobSeeker')
        if len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role=role)
        token = AuthToken.objects.create(user)[1]
        return Response({
            'token': token,
            'role': role,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        jobs = Job.objects.filter(user=request.user)
        job_serializer = JobSerializer(jobs, many=True)
        return Response({'profile': serializer.data, 'jobs': job_serializer.data})

class Contact(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message received successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ContactList(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)