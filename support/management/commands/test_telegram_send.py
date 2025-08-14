from django.core.management.base import BaseCommand
from support.client import TelegramBotClient
import asyncio


class Command(BaseCommand):
    help = 'Test sending a simple message to Telegram group'

    def handle(self, *args, **options):
        self.stdout.write('Testing Telegram bot send functionality...')
        
        try:
            client = TelegramBotClient()
            
            # Check configuration
            if not client.bot_token:
                self.stdout.write(self.style.ERROR('❌ TELEGRAM_BOT_TOKEN not configured'))
                return
                
            if not client.support_chat_id:
                self.stdout.write(self.style.ERROR('❌ TELEGRAM_SUPPORT_CHAT_ID not configured'))
                return
            
            self.stdout.write(f'✅ Bot token configured: {client.bot_token[:10]}...')
            self.stdout.write(f'✅ Chat ID configured: {client.support_chat_id}')
            
            # Send test message
            test_message = "🤖 **Test Message**\n\nHi! This is a test message from your Django support bot.\n\nIf you see this, the bot is working correctly! ✅"
            
            asyncio.run(client._send_message_async(test_message))
            
            self.stdout.write(self.style.SUCCESS('✅ Test message sent successfully!'))
            self.stdout.write('Check your Telegram group for the message.')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
