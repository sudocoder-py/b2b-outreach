from django.core.management.base import BaseCommand
from support.client import set_webhook


class Command(BaseCommand):
    help = 'Set Telegram webhook URL'

    def add_arguments(self, parser):
        parser.add_argument('webhook_url', type=str, help='The webhook URL to set')

    def handle(self, *args, **options):
        webhook_url = options['webhook_url']
        self.stdout.write(f'Setting webhook to: {webhook_url}')
        set_webhook(webhook_url)
        self.stdout.write(self.style.SUCCESS('Webhook set successfully!'))
