"""
URL configuration for jobboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jobs.views import JobList, JobCreate, Login, Register, Profile, Contact, ContactList
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/jobs/', JobList.as_view(), name='job-list'),
    path('api/jobs/create/', JobCreate.as_view(), name='job-create'),
    path('api/auth/login/', Login.as_view(), name='login'),
    path('api/auth/register/', Register.as_view(), name='register'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/profile/', Profile.as_view(), name='profile'),
    path('api/contact/', Contact.as_view(), name='contact'),
    path('api/contact/list/', ContactList.as_view(), name='contact-list'),  # Admin only
]
