from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id' ,'title', 'company', 'salary', 'position', 'last_date', 'is_active', 'is_verified', 'is_approved', 'is_soft_deleted']
    list_filter = ['is_active', 'is_verified', 'is_approved']
    search_fields = ['title', 'company']
    ordering = ['-created_at']
    list_editable = ['is_active', 'is_verified', 'is_approved', 'is_soft_deleted']
