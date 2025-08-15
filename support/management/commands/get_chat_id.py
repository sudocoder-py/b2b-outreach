from django.core.management.base import BaseCommand
from telegram import Bot
from django.conf import settings
import asyncio


class Command(BaseCommand):
    help = 'Get chat ID by sending a message to the bot and checking updates'

    def handle(self, *args, **options):
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        
        if not bot_token:
            self.stdout.write(self.style.ERROR('❌ TELEGRAM_BOT_TOKEN not configured'))
            return
        
        self.stdout.write('🔍 Getting chat updates to find your group chat ID...')
        self.stdout.write('')
        self.stdout.write('📋 INSTRUCTIONS:')
        self.stdout.write('1. Add your bot to your support group (if not already added)')
        self.stdout.write('2. Make your bot an admin in the group')
        self.stdout.write('3. Send any message in the group (like "test")')
        self.stdout.write('4. Run this command within a few minutes')
        self.stdout.write('')
        
        try:
            bot = Bot(token=bot_token)
            
            async def get_updates():
                updates = await bot.get_updates()
                
                if not updates:
                    self.stdout.write(self.style.WARNING('⚠️  No recent updates found.'))
                    self.stdout.write('Make sure you:')
                    self.stdout.write('- Added the bot to your group')
                    self.stdout.write('- Made the bot an admin')
                    self.stdout.write('- Sent a recent message in the group')
                    return
                
                self.stdout.write('📨 Recent updates:')
                self.stdout.write('-' * 50)
                
                for update in updates[-10:]:  # Show last 10 updates
                    if update.message:
                        chat = update.message.chat
                        chat_type = chat.type
                        chat_id = chat.id
                        chat_title = getattr(chat, 'title', 'N/A')
                        
                        if chat_type in ['group', 'supergroup']:
                            self.stdout.write(self.style.SUCCESS(f'🎯 GROUP FOUND:'))
                            self.stdout.write(f'   Chat ID: {chat_id}')
                            self.stdout.write(f'   Title: {chat_title}')
                            self.stdout.write(f'   Type: {chat_type}')
                            self.stdout.write('')
                            self.stdout.write(f'✅ Use this in your .env file:')
                            self.stdout.write(f'TELEGRAM_SUPPORT_CHAT_ID={chat_id}')
                            self.stdout.write('')
                        else:
                            self.stdout.write(f'💬 Private chat: {chat_id} (not a group)')
                
            asyncio.run(get_updates())
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
