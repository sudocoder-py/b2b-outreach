from django.core.management.base import BaseCommand
from campaign.email_sender import reset_daily_email_counts
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Reset daily email counts for all email accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting daily email count reset...'))
        
        try:
            updated_count = reset_daily_email_counts()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully reset daily email counts for {updated_count} email accounts'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error resetting daily email counts: {str(e)}')
            )
            logger.error(f'Error in reset_daily_email_counts command: {str(e)}')
