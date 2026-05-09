from django.contrib import admin
from .models import ResearchPost, Collaboration

@admin.register(ResearchPost)
class ResearchPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'researcher', 'field', 'status', 'views_count', 'created_at')
    list_filter = ('status', 'field')
    search_fields = ('title', 'researcher__email', 'tags')

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    # We changed 'research' to 'researcher' and 'topic' here
    list_display = ('student', 'researcher', 'topic', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__email', 'researcher__email', 'topic')