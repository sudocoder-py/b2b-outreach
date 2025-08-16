from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import serializers
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
from .helpers import extract_telegram_fields

from .models import ChatSession, Message
from .client import TelegramBotClient

logger = logging.getLogger(__name__)


# Serializers
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_type', 'content', 'created_at', 'support_agent_name', 'is_read']
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'created_at', 'updated_at', 'is_active', 'page_url', 'subject', 'messages', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class CreateMessageSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(required=False)

    class Meta:
        model = Message
        fields = ['session_id', 'message_type', 'content']

    def create(self, validated_data):
        user = self.context['request'].user
        session_id = validated_data.pop('session_id', None)

        # Get or create chat session
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=user)
        else:
            # Create new session
            session = ChatSession.objects.create(
                user=user,
                page_url=self.context['request'].data.get('page_url', ''),
                subject=self.context['request'].data.get('subject', '')
            )

        # Create the message
        message = Message.objects.create(
            session=session,
            sender='user',
            **validated_data
        )

        # Forward to Telegram
        try:
            logger.info(f"Attempting to forward message {message.id} to Telegram...")
            bot_client = TelegramBotClient()
            logger.info(f"Bot client created. Token configured: {bool(bot_client.bot_token)}, Chat ID configured: {bool(bot_client.support_chat_id)}")
            bot_client.forward_user_message(message)
            logger.info(f"Message {message.id} forwarded to Telegram successfully")
        except Exception as e:
            logger.error(f"Failed to forward message to Telegram: {e}")
            import traceback
            logger.error(traceback.format_exc())

        return message


# API Views
class CreateUserMessageView(generics.CreateAPIView):
    """
    Create a new user message and optionally start a new chat session.
    """
    serializer_class = CreateMessageSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        # Return the message with session info
        response_data = {
            'message': MessageSerializer(message).data,
            'session_id': str(message.session.id),
            'session_url': message.session.session_url
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class ChatSessionListView(generics.ListAPIView):
    """
    List all chat sessions for the authenticated user.
    """
    serializer_class = ChatSessionSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class ChatSessionDetailView(generics.RetrieveAPIView):
    """
    Get details of a specific chat session with all messages.
    """
    serializer_class = ChatSessionSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class ChatMessagesListView(generics.ListAPIView):
    """
    List all messages for a specific chat session.
    """
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        session = get_object_or_404(ChatSession, id=session_id, user=self.request.user)
        return session.messages.all()


# Webhook endpoint for Telegram bot
@api_view(['POST'])
@permission_classes([AllowAny])  # We'll handle authentication differently for webhook
def telegram_webhook(request):
    """
    Webhook endpoint for Telegram bot to post support replies.
    """
    # Simple API key authentication for webhook
    # api_key = request.headers.get('X-API-Key')
    # expected_key = getattr(settings, 'TELEGRAM_WEBHOOK_API_KEY', 'your-secret-key')

    # # Debug logging
    # logger.info(f"Webhook called. API Key received: {api_key[:10] + '...' if api_key else 'None'}")
    # logger.info(f"Expected API Key: {expected_key[:10] + '...' if expected_key else 'None'}")

    # if api_key != expected_key:
    #     logger.error(f"API key mismatch. Received: {api_key}, Expected: {expected_key}")
    #     return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    logger.info('Webhook called.')
    data = extract_telegram_fields(request.body)

    try:
        session_id = data.get('session_id')
        content = data.get('content')
        support_agent_name = data.get('support_agent_name', 'Support Team')
        telegram_user_id = data.get('telegram_user_id')
        message_type = data.get('message_type', 'text')
        
        if not session_id or not content:
            return Response({'error': 'session_id and content are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the session
        session = get_object_or_404(ChatSession, id=session_id)

        # Create support message
        message = Message.objects.create(
            session=session,
            sender='support',
            message_type=message_type,
            content=content,
            support_agent_name=support_agent_name,
            telegram_user_id=telegram_user_id
        )

        # Update session timestamp
        session.save()  # This will update the updated_at field

        return Response({
            'success': True,
            'message_id': str(message.id)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Test view for chat integration
@login_required
def test_chat_integration(request):
    """Test page for the chat integration"""
    return render(request, 'support/test_chat_integration.html')


# Chat session view
@login_required
def chat_session_view(request, session_id):
    """View a specific chat session"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    return render(request, 'support/chat_session.html', {'session': session})