from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Job, ContactMessage

# Register UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

# Register Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'user', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'company', 'location')
    date_hierarchy = 'created_at'

# Register ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'created_at'
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "Mark selected messages as resolved"