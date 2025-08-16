from django.core.management.base import BaseCommand
from django.conf import settings
from support.models import ChatSession, Message
from support.client import TelegramBotClient
import requests
import json


class Command(BaseCommand):
    help = 'Debug Telegram bot integration'

    def add_arguments(self, parser):
        parser.add_argument('--check-webhook', action='store_true', help='Check webhook status')
        parser.add_argument('--test-webhook', action='store_true', help='Test webhook endpoint')
        parser.add_argument('--check-sessions', action='store_true', help='Check recent chat sessions')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Telegram Bot Debug Information'))
        self.stdout.write('=' * 50)
        
        # Basic configuration check
        self.check_configuration()
        
        if options['check_webhook']:
            self.check_webhook_status()
        
        if options['test_webhook']:
            self.test_webhook_endpoint()
            
        if options['check_sessions']:
            self.check_recent_sessions()

    def check_configuration(self):
        self.stdout.write('\n📋 Configuration Check:')
        
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        chat_id = getattr(settings, 'TELEGRAM_SUPPORT_CHAT_ID', None)
        api_url = getattr(settings, 'DJANGO_API_URL', None)
        webhook_key = getattr(settings, 'TELEGRAM_WEBHOOK_API_KEY', None)
        
        self.stdout.write(f'✅ Bot Token: {"✓ Configured" if bot_token else "❌ Missing"}')
        self.stdout.write(f'✅ Chat ID: {chat_id if chat_id else "❌ Missing"}')
        self.stdout.write(f'✅ API URL: {api_url if api_url else "❌ Missing"}')
        self.stdout.write(f'✅ Webhook Key: {"✓ Configured" if webhook_key else "❌ Missing"}')

    def check_webhook_status(self):
        self.stdout.write('\n🔗 Webhook Status:')
        
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not bot_token:
            self.stdout.write(self.style.ERROR('❌ No bot token configured'))
            return
        
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            response = requests.get(url)
            data = response.json()
            
            if data.get('ok'):
                result = data.get('result', {})
                webhook_url = result.get('url', 'Not set')
                pending_updates = result.get('pending_update_count', 0)
                last_error = result.get('last_error_message', 'None')
                
                self.stdout.write(f'📍 Webhook URL: {webhook_url}')
                self.stdout.write(f'📊 Pending Updates: {pending_updates}')
                self.stdout.write(f'❗ Last Error: {last_error}')
                
                expected_url = f"{getattr(settings, 'DJANGO_API_URL', '')}/support/webhook/telegram/"
                if webhook_url == expected_url:
                    self.stdout.write(self.style.SUCCESS('✅ Webhook URL is correct'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️  Expected: {expected_url}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ API Error: {data}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error checking webhook: {e}'))

    def test_webhook_endpoint(self):
        self.stdout.write('\n🧪 Testing Webhook Endpoint:')
        
        api_url = getattr(settings, 'DJANGO_API_URL', 'http://localhost:8000')
        webhook_key = getattr(settings, 'TELEGRAM_WEBHOOK_API_KEY', '')
        
        # Get a recent session for testing
        recent_session = ChatSession.objects.first()
        if not recent_session:
            self.stdout.write(self.style.WARNING('⚠️  No chat sessions found. Create one first.'))
            return
        
        webhook_url = f"{api_url}/support/webhook/telegram/"
        headers = {
            'X-API-Key': webhook_key,
            'Content-Type': 'application/json'
        }
        data = {
            'session_id': str(recent_session.id),
            'content': 'Test message from debug command',
            'support_agent_name': 'Debug Bot',
            'telegram_user_id': 123456789,
            'message_type': 'text'
        }
        
        try:
            self.stdout.write(f'📡 Testing: {webhook_url}')
            response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
            
            self.stdout.write(f'📊 Status Code: {response.status_code}')
            self.stdout.write(f'📄 Response: {response.text}')
            
            if response.status_code == 201:
                self.stdout.write(self.style.SUCCESS('✅ Webhook test successful!'))
            else:
                self.stdout.write(self.style.ERROR('❌ Webhook test failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error testing webhook: {e}'))

    def check_recent_sessions(self):
        self.stdout.write('\n💬 Recent Chat Sessions:')
        
        sessions = ChatSession.objects.order_by('-created_at')[:5]
        
        if not sessions:
            self.stdout.write('📭 No chat sessions found')
            return
        
        for session in sessions:
            message_count = session.messages.count()
            user_messages = session.messages.filter(sender='user').count()
            support_messages = session.messages.filter(sender='support').count()
            
            self.stdout.write(f'\n🗨️  Session: {session.id}')
            self.stdout.write(f'   👤 User: {session.user.username}')
            self.stdout.write(f'   📅 Created: {session.created_at}')
            self.stdout.write(f'   📊 Messages: {message_count} (👤 {user_messages}, 🎧 {support_messages})')
            self.stdout.write(f'   🔄 Active: {session.is_active}')
            
            if session.subject:
                self.stdout.write(f'   📝 Subject: {session.subject}')

        self.stdout.write(f'\n📈 Total Sessions: {ChatSession.objects.count()}')
        self.stdout.write(f'📈 Total Messages: {Message.objects.count()}')
        
        # Check for sessions with no support replies
        sessions_without_replies = ChatSession.objects.filter(
            messages__sender='user'
        ).exclude(
            messages__sender='support'
        ).distinct().count()
        
        if sessions_without_replies > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  {sessions_without_replies} sessions have no support replies'))
