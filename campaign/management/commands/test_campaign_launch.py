from django.core.management.base import BaseCommand
from campaign.models import Campaign, CampaignOptions, MessageAssignment
from clients.models import EmailAccount
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test campaign launch functionality and debug issues'

    def add_arguments(self, parser):
        parser.add_argument('--campaign-id', type=int, required=True, help='Campaign ID to test')
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    def handle(self, *args, **options):
        campaign_id = options['campaign_id']
        verbose = options['verbose']
        
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        
        self.stdout.write(f'🚀 Testing campaign launch for campaign ID: {campaign_id}')
        
        try:
            # Step 1: Check if campaign exists
            self.stdout.write('\n📋 Step 1: Checking campaign...')
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                self.stdout.write(self.style.SUCCESS(f'✅ Campaign found: {campaign.name}'))
                self.stdout.write(f'   Status: {campaign.status}')
                self.stdout.write(f'   Product: {campaign.product.name}')
            except Campaign.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Campaign with ID {campaign_id} not found'))
                return
            
            # Step 2: Check campaign options
            self.stdout.write('\n⚙️ Step 2: Checking campaign options...')
            campaign_options = campaign.campaign_options.first()
            if not campaign_options:
                self.stdout.write(self.style.ERROR('❌ No campaign options found'))
                self.stdout.write('   💡 Create campaign options first')
                return
            else:
                self.stdout.write(self.style.SUCCESS(f'✅ Campaign options found (ID: {campaign_options.id})'))
                self.stdout.write(f'   Daily limit: {campaign_options.daily_limit}')
                self.stdout.write(f'   Stop on reply: {campaign_options.stop_on_reply}')
                self.stdout.write(f'   Open tracking: {campaign_options.open_tracking_enabled}')
            
            # Step 3: Check email accounts
            self.stdout.write('\n📧 Step 3: Checking email accounts...')
            email_accounts = campaign_options.email_accounts.all()
            if not email_accounts.exists():
                self.stdout.write(self.style.ERROR('❌ No email accounts assigned to campaign'))
                self.stdout.write('   💡 Assign email accounts to campaign options')
                return
            
            self.stdout.write(self.style.SUCCESS(f'✅ Found {email_accounts.count()} email accounts'))
            
            active_accounts = email_accounts.filter(status='active')
            for account in email_accounts:
                status_icon = '✅' if account.status == 'active' else '❌'
                self.stdout.write(f'   {status_icon} {account.email} - Status: {account.status}')
                self.stdout.write(f'      Daily usage: {account.emails_sent}/{account.daily_limit}')
                self.stdout.write(f'      Connection: {account.connection_type}')
                
                if account.is_smtp():
                    self.stdout.write(f'      SMTP: {account.smtp_host}:{account.smtp_port}')
            
            if not active_accounts.exists():
                self.stdout.write(self.style.ERROR('❌ No active email accounts found'))
                self.stdout.write('   💡 Activate at least one email account')
                return
            
            # Step 4: Check message assignments
            self.stdout.write('\n📝 Step 4: Checking message assignments...')
            total_assignments = MessageAssignment.objects.filter(campaign=campaign).count()
            pending_assignments = MessageAssignment.objects.filter(campaign=campaign, sent=False).count()
            personalized_assignments = MessageAssignment.objects.filter(
                campaign=campaign, 
                personlized_msg_to_send__gt=''
            ).count()
            
            self.stdout.write(f'   Total assignments: {total_assignments}')
            self.stdout.write(f'   Pending assignments: {pending_assignments}')
            self.stdout.write(f'   Personalized assignments: {personalized_assignments}')
            
            if total_assignments == 0:
                self.stdout.write(self.style.ERROR('❌ No message assignments found'))
                self.stdout.write('   💡 Create message assignments first')
                return
            
            if pending_assignments == 0:
                self.stdout.write(self.style.WARNING('⚠️ No pending message assignments'))
                self.stdout.write('   💡 All messages may have already been sent')
            
            # Step 5: Test email account connection
            self.stdout.write('\n🔌 Step 5: Testing email account connections...')
            for account in active_accounts:
                self.stdout.write(f'   Testing {account.email}...')
                try:
                    result = account.test_connection()
                    if result['success']:
                        self.stdout.write(self.style.SUCCESS(f'   ✅ {result["message"]}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'   ❌ {result["message"]}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ Connection test failed: {str(e)}'))
            
            # Step 6: Summary and recommendations
            self.stdout.write('\n📊 Summary:')
            
            ready_to_launch = True
            issues = []
            
            if not active_accounts.exists():
                ready_to_launch = False
                issues.append('No active email accounts')
            
            if pending_assignments == 0:
                ready_to_launch = False
                issues.append('No pending message assignments')
            
            # Check if any account has remaining capacity
            has_capacity = any(acc.emails_sent < acc.daily_limit for acc in active_accounts)
            if not has_capacity:
                ready_to_launch = False
                issues.append('All email accounts have reached daily limits')
            
            if ready_to_launch:
                self.stdout.write(self.style.SUCCESS('🎉 Campaign is ready to launch!'))
                self.stdout.write('\n💡 To launch the campaign:')
                self.stdout.write('   1. Go to campaign options page')
                self.stdout.write('   2. Click "Launch Campaign" button')
                self.stdout.write('   3. Or use API: POST /api/campaigns/{}/launch/'.format(campaign_id))
            else:
                self.stdout.write(self.style.ERROR('❌ Campaign is NOT ready to launch'))
                self.stdout.write('\n🔧 Issues to fix:')
                for issue in issues:
                    self.stdout.write(f'   • {issue}')
            
            # Step 7: Show API test command
            self.stdout.write('\n🧪 API Test Command:')
            self.stdout.write(f'curl -X POST http://localhost:8000/api/campaigns/{campaign_id}/launch/ \\')
            self.stdout.write('     -H "Content-Type: application/json" \\')
            self.stdout.write('     -H "X-CSRFToken: YOUR_CSRF_TOKEN"')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'💥 Error during testing: {str(e)}'))
            import traceback
            if verbose:
                self.stdout.write(traceback.format_exc())
