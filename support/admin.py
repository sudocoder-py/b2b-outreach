from django.contrib import admin
from .models import ChatSession, Message


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'is_active', 'created_at', 'message_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'subject']
    readonly_fields = ['id', 'created_at', 'updated_at', 'session_url']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'sender', 'message_type', 'created_at', 'support_agent_name', 'is_read']
    list_filter = ['sender', 'message_type', 'is_read', 'created_at']
    search_fields = ['session__user__username', 'content', 'support_agent_name']
    readonly_fields = ['id', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session__user')
