from django.core.management.base import BaseCommand
from clients.models import EmailAccount
from campaign.email_sender import test_email_account_connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email account connections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--account-id', 
            type=int, 
            help='Test specific email account by ID'
        )
        parser.add_argument(
            '--email', 
            type=str, 
            help='Test specific email account by email address'
        )

    def handle(self, *args, **options):
        account_id = options.get('account_id')
        email = options.get('email')
        
        if account_id:
            # Test specific account by ID
            try:
                account = EmailAccount.objects.get(id=account_id)
                self.test_single_account(account)
            except EmailAccount.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Email account with ID {account_id} not found')
                )
                
        elif email:
            # Test specific account by email
            try:
                account = EmailAccount.objects.get(email=email)
                self.test_single_account(account)
            except EmailAccount.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Email account with email {email} not found')
                )
                
        else:
            # Test all active accounts
            accounts = EmailAccount.objects.filter(status='active')
            if not accounts.exists():
                self.stdout.write(
                    self.style.WARNING('No active email accounts found')
                )
                return
                
            self.stdout.write(f'Testing {accounts.count()} active email accounts...\n')
            
            for account in accounts:
                self.test_single_account(account)
                
    def test_single_account(self, account):
        """Test a single email account"""
        self.stdout.write(f'Testing {account.email} ({account.connection_type})...')
        
        result = test_email_account_connection(account)
        
        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f'✓ {result["message"]}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'✗ {result["message"]}')
            )
        
        self.stdout.write('')  # Empty line for readability
