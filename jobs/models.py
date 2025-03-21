from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES = (('Employer', 'Employer'), ('JobSeeker', 'Job Seeker'), ('Admin', 'Admin'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='JobSeeker')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Job(models.Model):
    JOB_TYPES = (('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Internship', 'Internship'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES, default='Full-Time')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"