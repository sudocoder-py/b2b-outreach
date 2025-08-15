from django.db import models
from django.conf import settings
import uuid


class ChatSession(models.Model):
    """
    Represents a support chat session for a user.
    Each session has a unique ID and tracks the conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')

    # Session metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Optional session context
    page_url = models.URLField(blank=True, null=True, help_text="URL where the chat was initiated")
    subject = models.CharField(max_length=255, blank=True, help_text="Optional subject/topic of the chat")

    # Telegram-specific fields
    telegram_message_id = models.IntegerField(blank=True, null=True, help_text="ID of the initial message in Telegram group")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat Session {self.id} - {self.user.username}"

    @property
    def session_url(self):
        """Generate a URL for this chat session"""
        from django.conf import settings
        return f"{settings.SITE_URL}/support/chat/{self.id}/"


class Message(models.Model):
    """
    Represents individual messages within a chat session.
    Can be from user or support team.
    """
    SENDER_CHOICES = [
        ('user', 'User'),
        ('support', 'Support Team'),
    ]

    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')

    # Message content
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField(help_text="Text content or file URL")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    # Support team specific fields
    support_agent_name = models.CharField(max_length=100, blank=True, help_text="Name of support agent who replied")
    telegram_user_id = models.BigIntegerField(blank=True, null=True, help_text="Telegram user ID of support agent")

    # Message status
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} - {self.session.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"