from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # User API endpoints
    path('api/messages/', views.CreateUserMessageView.as_view(), name='create-message'),
    path('api/sessions/', views.ChatSessionListView.as_view(), name='session-list'),
    path('api/sessions/<uuid:pk>/', views.ChatSessionDetailView.as_view(), name='session-detail'),
    path('api/sessions/<uuid:session_id>/messages/', views.ChatMessagesListView.as_view(), name='session-messages'),

    # Telegram webhook
    path('webhook/telegram/', views.telegram_webhook, name='telegram-webhook'),

    # Frontend views
    path('test/', views.test_chat_integration, name='test-chat-integration'),
    path('chat/<uuid:session_id>/', views.chat_session_view, name='chat-session'),
]