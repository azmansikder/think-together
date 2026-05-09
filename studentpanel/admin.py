from django.contrib import admin
from .models import Project, SavedResearch, Message

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'field', 'status', 'created_at')
    list_filter = ('status', 'field')
    search_fields = ('title', 'student__email')


@admin.register(SavedResearch)
class SavedResearchAdmin(admin.ModelAdmin):
    list_display = ('student', 'research', 'saved_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_read', 'created_at')
    list_filter = ('is_read',)
