from django.core.management.base import BaseCommand
from support.client import set_webhook
from django.conf import settings


class Command(BaseCommand):
    help = 'Set Telegram webhook URL'

    def add_arguments(self, parser):
        parser.add_argument('--webhook-url', type=str, help='The webhook URL to set (optional, will use DJANGO_API_URL if not provided)')

    def handle(self, *args, **options):
        webhook_url = options.get('webhook_url')

        if not webhook_url:
            # Auto-generate webhook URL from settings
            django_api_url = getattr(settings, 'DJANGO_API_URL', 'http://localhost:8000')
            webhook_url = f"{django_api_url}/support/webhook/telegram/"

        self.stdout.write(f'Setting webhook to: {webhook_url}')
        set_webhook(webhook_url)
        self.stdout.write(self.style.SUCCESS('Webhook set successfully!'))
