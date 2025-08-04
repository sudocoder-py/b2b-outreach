from django.core.management.base import BaseCommand
from campaign.tasks import personalize_and_send_all_emails_at_once
from campaign.models import Campaign
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test Celery task serialization for campaign launch'

    def add_arguments(self, parser):
        parser.add_argument('--campaign-id', type=int, required=True, help='Campaign ID to test')
        parser.add_argument('--dry-run', action='store_true', help='Test serialization without actually running tasks')

    def handle(self, *args, **options):
        campaign_id = options['campaign_id']
        dry_run = options['dry_run']
        
        self.stdout.write(f'🧪 Testing Celery serialization for campaign ID: {campaign_id}')
        
        try:
            # Check if campaign exists
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                self.stdout.write(self.style.SUCCESS(f'✅ Campaign found: {campaign.name}'))
            except Campaign.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Campaign with ID {campaign_id} not found'))
                return
            
            if dry_run:
                self.stdout.write('🔍 Dry run mode - testing serialization only...')
                
                # Test if we can serialize the task arguments
                try:
                    import json
                    
                    # Test serializing campaign_id (should work)
                    serialized_id = json.dumps(campaign_id)
                    self.stdout.write(f'✅ Campaign ID serialization test passed: {serialized_id}')
                    
                    # Test serializing campaign object (should fail)
                    try:
                        serialized_campaign = json.dumps(campaign)
                        self.stdout.write(self.style.ERROR('❌ Campaign object serialization should have failed but passed'))
                    except TypeError as e:
                        self.stdout.write(self.style.SUCCESS(f'✅ Campaign object serialization correctly failed: {str(e)}'))
                    
                    self.stdout.write('✅ Serialization tests passed - ready for Celery')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Serialization test failed: {str(e)}'))
                    return
            else:
                self.stdout.write('🚀 Running actual Celery task...')
                
                # Run the actual task
                try:
                    task_result = personalize_and_send_all_emails_at_once.delay(campaign_id)
                    self.stdout.write(self.style.SUCCESS(f'✅ Task started successfully'))
                    self.stdout.write(f'   Task ID: {task_result.id}')
                    self.stdout.write(f'   Task State: {task_result.state}')
                    
                    # Wait a bit and check result
                    import time
                    time.sleep(2)
                    
                    if task_result.ready():
                        result = task_result.result
                        self.stdout.write(f'   Task Result: {result}')
                        
                        if isinstance(result, dict) and result.get('status') == 'success':
                            self.stdout.write(self.style.SUCCESS('🎉 Task completed successfully!'))
                        else:
                            self.stdout.write(self.style.WARNING(f'⚠️ Task completed with issues: {result}'))
                    else:
                        self.stdout.write('⏳ Task is still running in background')
                        self.stdout.write('   Check Celery worker logs for progress')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Task failed to start: {str(e)}'))
                    import traceback
                    self.stdout.write(traceback.format_exc())
            
            self.stdout.write('\n💡 Tips:')
            self.stdout.write('   • Make sure Celery worker is running: celery -A dcrm worker -l info')
            self.stdout.write('   • Check worker logs for detailed task execution')
            self.stdout.write('   • Use --dry-run to test serialization without running tasks')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'💥 Error during testing: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
