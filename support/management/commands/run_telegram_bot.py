from django.core.management.base import BaseCommand
from support.client import run_bot_polling


class Command(BaseCommand):
    help = 'Run Telegram bot in polling mode'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))
        try:
            run_bot_polling()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Bot stopped.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Bot error: {e}'))
