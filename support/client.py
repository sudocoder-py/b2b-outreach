import logging
import requests
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
from typing import Optional
import json

logger = logging.getLogger(__name__)


class TelegramBotClient:
    """
    Telegram bot client for handling support chat integration.
    """

    def __init__(self):
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.support_chat_id = getattr(settings, 'TELEGRAM_SUPPORT_CHAT_ID', None)
        self.django_api_url = getattr(settings, 'DJANGO_API_URL', 'http://localhost:8000')
        self.webhook_api_key = getattr(settings, 'TELEGRAM_WEBHOOK_API_KEY', 'your-secret-key')

        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not configured")
            return

        self.bot = Bot(token=self.bot_token)

    def forward_user_message(self, message):
        """
        Forward a user message to the Telegram support group.
        """
        logger.info(f"forward_user_message called for message {message.id}")
        logger.info(f"Bot token configured: {bool(self.bot_token)}")
        logger.info(f"Support chat ID configured: {bool(self.support_chat_id)}")

        if not self.bot_token or not self.support_chat_id:
            logger.error("Telegram bot not properly configured")
            logger.error(f"Bot token: {self.bot_token[:10] + '...' if self.bot_token else 'None'}")
            logger.error(f"Chat ID: {self.support_chat_id}")
            return

        try:
            # Format the message for Telegram
            user = message.session.user
            session_url = message.session.session_url

            telegram_text = f"""
🆘 **New Support Message**

👤 **User:** {user.username} ({user.email})
🆔 **Session ID:** `{message.session.id}`
🔗 **Session URL:** {session_url}
📄 **Page:** {message.session.page_url or 'N/A'}
📝 **Subject:** {message.session.subject or 'N/A'}

💬 **Message:**
{message.content}

---
Reply with: `/reply {message.session.id} <your response>`
            """.strip()

            # Send message to support group
            asyncio.run(self._send_message_async(telegram_text))

        except Exception as e:
            logger.error(f"Failed to forward message to Telegram: {e}")

    async def _send_message_async(self, text: str):
        """Send message asynchronously"""
        await self.bot.send_message(
            chat_id=self.support_chat_id,
            text=text,
            parse_mode='Markdown'
        )

    def setup_bot_handlers(self):
        """
        Set up bot handlers for processing support team replies.
        Use this for polling mode.
        """
        if not self.bot_token:
            logger.error("Cannot setup bot handlers: TELEGRAM_BOT_TOKEN not configured")
            return None

        # Build application with proper initialization
        application = Application.builder().token(self.bot_token).build()

        # Add handlers
        application.add_handler(CommandHandler("reply", self.handle_reply_command))
        application.add_handler(MessageHandler(filters.REPLY, self.handle_reply_message))
        application.add_handler(CommandHandler("start", self.handle_start_command))
        application.add_handler(CommandHandler("help", self.handle_help_command))

        return application

    async def handle_reply_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /reply command from support team.
        Format: /reply <session_id> <message>
        """
        try:
            if not context.args or len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: /reply <session_id> <your message>\n"
                    "Example: /reply 123e4567-e89b-12d3-a456-426614174000 Hello, how can I help you?"
                )
                return

            session_id = context.args[0]
            reply_text = ' '.join(context.args[1:])

            # Get support agent info
            support_agent_name = update.effective_user.full_name or update.effective_user.username or "Support Team"
            telegram_user_id = update.effective_user.id

            # Send to Django API
            success = await self._send_to_django_api(
                session_id=session_id,
                content=reply_text,
                support_agent_name=support_agent_name,
                telegram_user_id=telegram_user_id
            )

            if success:
                await update.message.reply_text("✅ Reply sent successfully!")
            else:
                await update.message.reply_text("❌ Failed to send reply. Please check the session ID.")

        except Exception as e:
            logger.error(f"Error handling reply command: {e}")
            await update.message.reply_text("❌ An error occurred while processing your reply.")

    async def handle_reply_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle replies to bot messages (alternative to /reply command).
        """
        try:
            # Check if this is a reply to a bot message
            if not update.message.reply_to_message:
                return

            # Get bot info to check if reply is to our bot
            bot_info = await context.bot.get_me()
            if update.message.reply_to_message.from_user.id != bot_info.id:
                return

            # Extract session ID from the original message
            original_text = update.message.reply_to_message.text
            if "Session ID:" not in original_text:
                await update.message.reply_text("❌ Could not find session ID in the original message.")
                return

            # Parse session ID
            lines = original_text.split('\n')
            session_id = None
            for line in lines:
                if "Session ID:" in line:
                    session_id = line.split('`')[1] if '`' in line else line.split(':')[1].strip()
                    break

            if not session_id:
                await update.message.reply_text("❌ Could not extract session ID.")
                return

            reply_text = update.message.text
            support_agent_name = update.effective_user.full_name or update.effective_user.username or "Support Team"
            telegram_user_id = update.effective_user.id

            # Send to Django API
            success = await self._send_to_django_api(
                session_id=session_id,
                content=reply_text,
                support_agent_name=support_agent_name,
                telegram_user_id=telegram_user_id
            )

            if success:
                await update.message.reply_text("✅ Reply sent successfully!")
            else:
                await update.message.reply_text("❌ Failed to send reply.")

        except Exception as e:
            logger.error(f"Error handling reply message: {e}")
            await update.message.reply_text("❌ An error occurred while processing your reply.")

    async def handle_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """
🤖 **Support Bot**

This bot forwards customer support messages to this group.

**How to reply:**
1. Use `/reply <session_id> <your message>`
2. Or simply reply to the bot's message

**Commands:**
/help - Show this help message
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    async def handle_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.handle_start_command(update, context)

    async def _send_to_django_api(self, session_id: str, content: str, support_agent_name: str, telegram_user_id: int) -> bool:
        """
        Send support reply to Django API.
        """
        try:
            url = f"{self.django_api_url}/support/webhook/telegram/"
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': self.webhook_api_key
            }
            data = {
                'session_id': session_id,
                'content': content,
                'support_agent_name': support_agent_name,
                'telegram_user_id': telegram_user_id,
                'message_type': 'text'
            }

            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code == 201

        except Exception as e:
            logger.error(f"Failed to send to Django API: {e}")
            return False


# Bot runner functions
def run_bot_polling():
    """
    Run the bot in polling mode.
    Use this for development or when webhooks are not available.
    """
    client = TelegramBotClient()
    application = client.setup_bot_handlers()

    if application:
        logger.info("Starting Telegram bot in polling mode...")
        application.run_polling()
    else:
        logger.error("Failed to start bot: configuration error")


def set_webhook(webhook_url: str):
    """
    Set up webhook for the bot.
    Use this for production deployment.
    """
    client = TelegramBotClient()
    if client.bot_token:
        try:
            asyncio.run(client.bot.set_webhook(url=webhook_url))
            logger.info(f"Webhook set to: {webhook_url}")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
    else:
        logger.error("Cannot set webhook: TELEGRAM_BOT_TOKEN not configured")