from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'completed', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'due_date')