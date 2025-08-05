from django.core.management.base import BaseCommand
from clients.models import EmailAccount
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically fix common SSL/TLS configuration issues for email accounts'

    def add_arguments(self, parser):
        parser.add_argument('--account-id', type=int, help='Fix specific email account by ID')
        parser.add_argument('--email', type=str, help='Fix specific email account by email')
        parser.add_argument('--fix-all', action='store_true', help='Fix all active email accounts')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')

    def handle(self, *args, **options):
        account_id = options.get('account_id')
        email = options.get('email')
        fix_all = options.get('fix_all')
        dry_run = options.get('dry_run')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No changes will be made'))
        
        if account_id:
            try:
                account = EmailAccount.objects.get(id=account_id)
                self.fix_account_config(account, dry_run)
            except EmailAccount.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Email account with ID {account_id} not found'))
                
        elif email:
            try:
                account = EmailAccount.objects.get(email=email)
                self.fix_account_config(account, dry_run)
            except EmailAccount.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Email account with email {email} not found'))
                
        elif fix_all:
            accounts = EmailAccount.objects.filter(status='active', connection_type='imap/smtp')
            if not accounts.exists():
                self.stdout.write(self.style.WARNING('⚠️ No active SMTP email accounts found'))
                return
                
            for account in accounts:
                self.stdout.write(f'\n{"="*50}')
                self.fix_account_config(account, dry_run)
                
        else:
            self.stdout.write(self.style.ERROR('❌ Please specify --account-id, --email, or --fix-all'))

    def fix_account_config(self, account, dry_run=False):
        """Fix SSL/TLS configuration for an email account"""
        self.stdout.write(f'🔧 Analyzing: {account.email}')
        self.stdout.write(f'   Current: Host={account.smtp_host}, Port={account.smtp_port}')
        self.stdout.write(f'   Current: TLS={account.smtp_use_tls}, SSL={account.smtp_use_ssl}')
        
        # Determine recommended configuration
        recommended_config = self.get_recommended_config(account)
        
        if not recommended_config:
            self.stdout.write('   ℹ️ No specific recommendations available for this configuration')
            return
        
        # Check if current config matches recommendation
        current_matches = (
            account.smtp_port == recommended_config['port'] and
            account.smtp_use_tls == recommended_config['tls'] and
            account.smtp_use_ssl == recommended_config['ssl']
        )
        
        if current_matches:
            self.stdout.write(self.style.SUCCESS('   ✅ Configuration already optimal'))
            return
        
        # Show recommended changes
        self.stdout.write(f'   💡 Recommended: Port={recommended_config["port"]}, TLS={recommended_config["tls"]}, SSL={recommended_config["ssl"]}')
        self.stdout.write(f'   📝 Reason: {recommended_config["reason"]}')
        
        if not dry_run:
            # Apply the changes
            account.smtp_port = recommended_config['port']
            account.smtp_use_tls = recommended_config['tls']
            account.smtp_use_ssl = recommended_config['ssl']
            account.save(update_fields=['smtp_port', 'smtp_use_tls', 'smtp_use_ssl'])
            
            self.stdout.write(self.style.SUCCESS('   ✅ Configuration updated successfully'))
            
            # Test the new configuration
            self.stdout.write('   🧪 Testing new configuration...')
            try:
                result = account.test_connection()
                if result['success']:
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Test successful: {result["message"]}'))
                else:
                    self.stdout.write(self.style.ERROR(f'   ❌ Test failed: {result["message"]}'))
                    self.stdout.write('   💡 You may need to check credentials or server settings')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Test error: {str(e)}'))
        else:
            self.stdout.write('   🔍 Would update configuration (dry run mode)')

    def get_recommended_config(self, account):
        """Get recommended SSL/TLS configuration based on host and current settings"""
        host_lower = account.smtp_host.lower()
        
        # Provider-specific recommendations
        if 'gmail' in host_lower:
            if account.smtp_port == 465:
                return {
                    'port': 465,
                    'tls': False,
                    'ssl': True,
                    'reason': 'Gmail port 465 requires SSL/TLS (not STARTTLS)'
                }
            else:
                return {
                    'port': 587,
                    'tls': True,
                    'ssl': False,
                    'reason': 'Gmail port 587 requires STARTTLS'
                }
                
        elif 'outlook' in host_lower or 'hotmail' in host_lower:
            return {
                'port': 587,
                'tls': True,
                'ssl': False,
                'reason': 'Outlook/Hotmail requires STARTTLS on port 587'
            }
            
        elif 'yahoo' in host_lower:
            if account.smtp_port == 465:
                return {
                    'port': 465,
                    'tls': False,
                    'ssl': True,
                    'reason': 'Yahoo port 465 requires SSL/TLS (not STARTTLS)'
                }
            else:
                return {
                    'port': 587,
                    'tls': True,
                    'ssl': False,
                    'reason': 'Yahoo port 587 requires STARTTLS'
                }
                
        elif 'zoho' in host_lower:
            if account.smtp_port == 465:
                return {
                    'port': 465,
                    'tls': False,
                    'ssl': True,
                    'reason': 'Zoho port 465 requires SSL/TLS (not STARTTLS)'
                }
            else:
                return {
                    'port': 587,
                    'tls': True,
                    'ssl': False,
                    'reason': 'Zoho port 587 requires STARTTLS'
                }
        
        # Generic recommendations based on port
        elif account.smtp_port == 587:
            return {
                'port': 587,
                'tls': True,
                'ssl': False,
                'reason': 'Port 587 typically requires STARTTLS'
            }
        elif account.smtp_port == 465:
            return {
                'port': 465,
                'tls': False,
                'ssl': True,
                'reason': 'Port 465 typically requires SSL/TLS'
            }
        elif account.smtp_port == 25:
            return {
                'port': 25,
                'tls': False,
                'ssl': False,
                'reason': 'Port 25 typically uses plain connection'
            }
        
        # Check for common misconfigurations
        elif account.smtp_use_tls and account.smtp_use_ssl:
            return {
                'port': account.smtp_port,
                'tls': True,
                'ssl': False,
                'reason': 'Both TLS and SSL enabled - using STARTTLS only'
            }
        
        return None
