from django.core.management.base import BaseCommand, CommandError
from clients.models import EmailAccount, SubscribedCompany
from campaign.email_utils import create_smtp_account, get_smtp_config_for_provider, validate_smtp_config
import getpass
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Set up a new email account for sending campaigns'

    def add_arguments(self, parser):
        parser.add_argument('--company-id', type=int, required=True, help='Company ID')
        parser.add_argument('--email', type=str, required=True, help='Email address')
        parser.add_argument('--provider', type=str, help='Email provider (gmail, outlook, yahoo, zoho)')
        parser.add_argument('--host', type=str, help='SMTP host')
        parser.add_argument('--port', type=int, help='SMTP port')
        parser.add_argument('--username', type=str, help='SMTP username (defaults to email)')
        parser.add_argument('--password', type=str, help='SMTP password (will prompt if not provided)')
        parser.add_argument('--use-tls', action='store_true', help='Use TLS encryption')
        parser.add_argument('--use-ssl', action='store_true', help='Use SSL encryption')
        parser.add_argument('--sender-name', type=str, help='Sender display name')
        parser.add_argument('--daily-limit', type=int, default=30, help='Daily email limit')
        parser.add_argument('--test-connection', action='store_true', help='Test connection after setup')

    def handle(self, *args, **options):
        try:
            # Get company
            company_id = options['company_id']
            try:
                company = SubscribedCompany.objects.get(id=company_id)
                self.stdout.write(f'Setting up email account for company: {company.name}')
            except SubscribedCompany.DoesNotExist:
                raise CommandError(f'Company with ID {company_id} not found')

            email = options['email']
            
            # Check if email account already exists
            if EmailAccount.objects.filter(email=email).exists():
                raise CommandError(f'Email account {email} already exists')

            # Build SMTP configuration
            smtp_config = {}
            
            if options['provider']:
                # Use predefined provider settings
                provider_config = get_smtp_config_for_provider(options['provider'])
                if not provider_config:
                    raise CommandError(f'Unknown provider: {options["provider"]}')
                smtp_config.update(provider_config)
                self.stdout.write(f'Using {options["provider"]} settings')
            
            # Override with manual settings if provided
            if options['host']:
                smtp_config['host'] = options['host']
            if options['port']:
                smtp_config['port'] = options['port']
            if options['use_tls']:
                smtp_config['use_tls'] = True
                smtp_config['use_ssl'] = False
            if options['use_ssl']:
                smtp_config['use_ssl'] = True
                smtp_config['use_tls'] = False

            # Set username and password
            smtp_config['username'] = options['username'] or email
            
            if options['password']:
                smtp_config['password'] = options['password']
            else:
                smtp_config['password'] = getpass.getpass(f'Enter password for {email}: ')

            # Validate configuration
            validation = validate_smtp_config(smtp_config)
            if not validation['valid']:
                for error in validation['errors']:
                    self.stdout.write(self.style.ERROR(f'Configuration error: {error}'))
                raise CommandError('Invalid SMTP configuration')

            # Build sender configuration
            sender_config = {
                'name': options['sender_name'] or '',
                'daily_limit': options['daily_limit']
            }

            # Create the account
            self.stdout.write('Creating email account...')
            account = create_smtp_account(company, email, smtp_config, sender_config)
            
            if not account:
                raise CommandError('Failed to create email account')

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created email account: {email}')
            )

            # Test connection if requested
            if options['test_connection']:
                self.stdout.write('Testing connection...')
                result = account.test_connection()
                
                if result['success']:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {result["message"]}')
                    )
                    # Update status to active if test successful
                    account.status = 'active'
                    account.save()
                    self.stdout.write('Account status updated to active')
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {result["message"]}')
                    )
                    account.status = 'error'
                    account.save()
                    self.stdout.write('Account status updated to error')

            # Display account details
            self.stdout.write('\nAccount Details:')
            self.stdout.write(f'  Email: {account.email}')
            self.stdout.write(f'  Status: {account.status}')
            self.stdout.write(f'  SMTP Host: {account.smtp_host}')
            self.stdout.write(f'  SMTP Port: {account.smtp_port}')
            self.stdout.write(f'  Use TLS: {account.smtp_use_tls}')
            self.stdout.write(f'  Use SSL: {account.smtp_use_ssl}')
            self.stdout.write(f'  Daily Limit: {account.daily_limit}')
            self.stdout.write(f'  Sender Name: {account.sender_name or "Not set"}')

        except Exception as e:
            logger.error(f'Error in setup_email_account command: {str(e)}')
            raise CommandError(f'Setup failed: {str(e)}')
