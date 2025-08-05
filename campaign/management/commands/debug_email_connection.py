from django.core.management.base import BaseCommand
from clients.models import EmailAccount
from campaign.email_sender import CustomEmailBackend
import smtplib
import ssl
import socket
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug email account SMTP connections with detailed SSL/TLS analysis'

    def add_arguments(self, parser):
        parser.add_argument('--account-id', type=int, help='Test specific email account by ID')
        parser.add_argument('--email', type=str, help='Test specific email account by email')
        parser.add_argument('--test-all', action='store_true', help='Test all active email accounts')

    def handle(self, *args, **options):
        account_id = options.get('account_id')
        email = options.get('email')
        test_all = options.get('test_all')
        
        if account_id:
            try:
                account = EmailAccount.objects.get(id=account_id)
                self.test_account_detailed(account)
            except EmailAccount.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Email account with ID {account_id} not found'))
                
        elif email:
            try:
                account = EmailAccount.objects.get(email=email)
                self.test_account_detailed(account)
            except EmailAccount.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Email account with email {email} not found'))
                
        elif test_all:
            accounts = EmailAccount.objects.filter(status='active', connection_type='imap/smtp')
            if not accounts.exists():
                self.stdout.write(self.style.WARNING('⚠️ No active SMTP email accounts found'))
                return
                
            for account in accounts:
                self.stdout.write(f'\n{"="*60}')
                self.test_account_detailed(account)
                
        else:
            self.stdout.write(self.style.ERROR('❌ Please specify --account-id, --email, or --test-all'))

    def test_account_detailed(self, account):
        """Perform detailed testing of an email account"""
        self.stdout.write(f'🔍 Testing Email Account: {account.email}')
        self.stdout.write(f'   Host: {account.smtp_host}')
        self.stdout.write(f'   Port: {account.smtp_port}')
        self.stdout.write(f'   Username: {account.smtp_username}')
        self.stdout.write(f'   TLS: {account.smtp_use_tls}')
        self.stdout.write(f'   SSL: {account.smtp_use_ssl}')
        
        # Step 1: Test basic connectivity
        self.stdout.write('\n🔌 Step 1: Testing basic connectivity...')
        if self.test_basic_connectivity(account):
            self.stdout.write(self.style.SUCCESS('✅ Basic connectivity: OK'))
        else:
            self.stdout.write(self.style.ERROR('❌ Basic connectivity: FAILED'))
            return
        
        # Step 2: Test SSL/TLS capabilities
        self.stdout.write('\n🔐 Step 2: Testing SSL/TLS capabilities...')
        self.test_ssl_tls_capabilities(account)
        
        # Step 3: Test Django backend
        self.stdout.write('\n🐍 Step 3: Testing Django email backend...')
        self.test_django_backend(account)
        
        # Step 4: Provide recommendations
        self.stdout.write('\n💡 Step 4: Configuration recommendations...')
        self.provide_recommendations(account)

    def test_basic_connectivity(self, account):
        """Test basic TCP connectivity to SMTP server"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((account.smtp_host, account.smtp_port))
            sock.close()
            return result == 0
        except Exception as e:
            self.stdout.write(f'   ❌ Connectivity error: {str(e)}')
            return False

    def test_ssl_tls_capabilities(self, account):
        """Test SSL/TLS capabilities of the SMTP server"""
        try:
            # Test different SSL/TLS configurations
            configs_to_test = [
                {'use_tls': True, 'use_ssl': False, 'name': 'STARTTLS'},
                {'use_tls': False, 'use_ssl': True, 'name': 'SSL/TLS'},
                {'use_tls': False, 'use_ssl': False, 'name': 'Plain'},
            ]
            
            for config in configs_to_test:
                self.stdout.write(f'   Testing {config["name"]}...')
                try:
                    if config['use_ssl']:
                        # Direct SSL connection
                        context = ssl.create_default_context()
                        server = smtplib.SMTP_SSL(account.smtp_host, account.smtp_port, context=context, timeout=10)
                    else:
                        # Plain connection, possibly with STARTTLS
                        server = smtplib.SMTP(account.smtp_host, account.smtp_port, timeout=10)
                        if config['use_tls']:
                            server.starttls()
                    
                    server.quit()
                    
                    # Check if this matches current config
                    if (config['use_tls'] == account.smtp_use_tls and 
                        config['use_ssl'] == account.smtp_use_ssl):
                        self.stdout.write(f'     ✅ {config["name"]}: OK (CURRENT CONFIG)')
                    else:
                        self.stdout.write(f'     ✅ {config["name"]}: OK')
                        
                except Exception as e:
                    if (config['use_tls'] == account.smtp_use_tls and 
                        config['use_ssl'] == account.smtp_use_ssl):
                        self.stdout.write(f'     ❌ {config["name"]}: FAILED (CURRENT CONFIG) - {str(e)}')
                    else:
                        self.stdout.write(f'     ❌ {config["name"]}: FAILED - {str(e)}')
                        
        except Exception as e:
            self.stdout.write(f'   ❌ SSL/TLS testing error: {str(e)}')

    def test_django_backend(self, account):
        """Test Django email backend"""
        try:
            backend = CustomEmailBackend(account)
            connection = backend.open()
            if connection:
                backend.close()
                self.stdout.write('   ✅ Django backend: OK')
                return True
            else:
                self.stdout.write('   ❌ Django backend: Connection failed')
                return False
        except Exception as e:
            self.stdout.write(f'   ❌ Django backend error: {str(e)}')
            return False

    def provide_recommendations(self, account):
        """Provide configuration recommendations based on common providers"""
        host_lower = account.smtp_host.lower()
        
        # Common provider recommendations
        recommendations = {
            'gmail.com': [
                {'port': 587, 'tls': True, 'ssl': False, 'desc': 'Gmail STARTTLS (recommended)'},
                {'port': 465, 'tls': False, 'ssl': True, 'desc': 'Gmail SSL/TLS'},
            ],
            'outlook.com': [
                {'port': 587, 'tls': True, 'ssl': False, 'desc': 'Outlook STARTTLS (recommended)'},
            ],
            'yahoo.com': [
                {'port': 587, 'tls': True, 'ssl': False, 'desc': 'Yahoo STARTTLS (recommended)'},
                {'port': 465, 'tls': False, 'ssl': True, 'desc': 'Yahoo SSL/TLS'},
            ],
        }
        
        # Find matching provider
        provider_found = False
        for provider, configs in recommendations.items():
            if provider in host_lower:
                provider_found = True
                self.stdout.write(f'   📧 Detected provider: {provider.title()}')
                self.stdout.write('   🔧 Recommended configurations:')
                
                for config in configs:
                    current = (config['port'] == account.smtp_port and 
                             config['tls'] == account.smtp_use_tls and 
                             config['ssl'] == account.smtp_use_ssl)
                    
                    status = '(CURRENT)' if current else ''
                    self.stdout.write(f'     • Port {config["port"]}, TLS={config["tls"]}, SSL={config["ssl"]} - {config["desc"]} {status}')
                break
        
        if not provider_found:
            self.stdout.write('   🔧 General recommendations:')
            self.stdout.write('     • Port 587: Usually requires TLS=True, SSL=False (STARTTLS)')
            self.stdout.write('     • Port 465: Usually requires TLS=False, SSL=True (SSL/TLS)')
            self.stdout.write('     • Port 25: Usually requires TLS=False, SSL=False (Plain)')
        
        # Current configuration analysis
        current_config = f'Port {account.smtp_port}, TLS={account.smtp_use_tls}, SSL={account.smtp_use_ssl}'
        self.stdout.write(f'   📊 Current configuration: {current_config}')
        
        # Common issues
        if account.smtp_port == 587 and account.smtp_use_ssl and not account.smtp_use_tls:
            self.stdout.write('   ⚠️ Warning: Port 587 with SSL=True is unusual. Try TLS=True, SSL=False')
        elif account.smtp_port == 465 and account.smtp_use_tls and not account.smtp_use_ssl:
            self.stdout.write('   ⚠️ Warning: Port 465 with TLS=True is unusual. Try TLS=False, SSL=True')
        elif account.smtp_use_tls and account.smtp_use_ssl:
            self.stdout.write('   ⚠️ Warning: Both TLS and SSL enabled. Usually only one should be True')
