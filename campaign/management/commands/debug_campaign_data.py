from django.core.management.base import BaseCommand
from campaign.models import Campaign, MessageAssignment
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug campaign data to identify issues with personalization'

    def add_arguments(self, parser):
        parser.add_argument('--campaign-id', type=int, required=True, help='Campaign ID to debug')

    def handle(self, *args, **options):
        campaign_id = options['campaign_id']
        
        self.stdout.write(f'🔍 Debugging campaign data for campaign ID: {campaign_id}')
        
        try:
            # Get campaign
            try:
                campaign = Campaign.objects.get(id=campaign_id)
                self.stdout.write(self.style.SUCCESS(f'✅ Campaign found: {campaign.name}'))
            except Campaign.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Campaign with ID {campaign_id} not found'))
                return
            
            # Check campaign dates
            self.stdout.write('\n📅 Campaign Dates:')
            self.stdout.write(f'   Start Date: {campaign.start_date}')
            self.stdout.write(f'   End Date: {campaign.end_date}')
            
            if campaign.start_date is None:
                self.stdout.write(self.style.WARNING('⚠️ Start date is None - this was causing the isoformat() error'))
            
            # Test campaign.to_dict_for_ai()
            self.stdout.write('\n🤖 Testing Campaign AI Data:')
            try:
                ai_data = campaign.to_dict_for_ai()
                self.stdout.write(self.style.SUCCESS('✅ Campaign AI data generation successful'))
                for key, value in ai_data.items():
                    self.stdout.write(f'   {key}: {value}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Campaign AI data generation failed: {str(e)}'))
            
            # Check message assignments
            self.stdout.write('\n📝 Message Assignments:')
            assignments = MessageAssignment.objects.filter(campaign=campaign)
            self.stdout.write(f'   Total assignments: {assignments.count()}')
            
            for i, assignment in enumerate(assignments[:5]):  # Show first 5
                self.stdout.write(f'\n   Assignment {i+1} (ID: {assignment.id}):')
                self.stdout.write(f'     Lead: {assignment.campaign_lead.lead.email}')
                self.stdout.write(f'     Message: {assignment.message.subject}')
                self.stdout.write(f'     Sent: {assignment.sent}')
                self.stdout.write(f'     Has personalized content: {"Yes" if assignment.personlized_msg_to_send else "No"}')
                
                # Test lead AI data
                try:
                    lead_ai_data = assignment.campaign_lead.lead.to_dict_for_ai()
                    self.stdout.write(f'     ✅ Lead AI data: OK')
                except Exception as e:
                    self.stdout.write(f'     ❌ Lead AI data error: {str(e)}')
                
                # Test assignment AI data
                try:
                    assignment_ai_data = assignment.to_dict_for_ai()
                    self.stdout.write(f'     ✅ Assignment AI data: OK')
                except Exception as e:
                    self.stdout.write(f'     ❌ Assignment AI data error: {str(e)}')
            
            if assignments.count() > 5:
                self.stdout.write(f'   ... and {assignments.count() - 5} more assignments')
            
            # Test personalization on first unpersonalized assignment
            self.stdout.write('\n🧪 Testing Personalization:')
            unpersonalized = assignments.filter(personlized_msg_to_send='').first()
            
            if unpersonalized:
                self.stdout.write(f'   Testing assignment ID: {unpersonalized.id}')
                try:
                    # Test with skip=True (no AI, just template replacement)
                    success = unpersonalized.personalize_with_ai(skip=True)
                    if success:
                        self.stdout.write(self.style.SUCCESS('   ✅ Personalization test successful'))
                        self.stdout.write(f'   Personalized content length: {len(unpersonalized.personlized_msg_to_send)}')
                    else:
                        self.stdout.write(self.style.ERROR('   ❌ Personalization test failed'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'   ❌ Personalization test error: {str(e)}'))
                    import traceback
                    self.stdout.write(f'   Full traceback: {traceback.format_exc()}')
            else:
                self.stdout.write('   No unpersonalized assignments found to test')
            
            # Summary
            self.stdout.write('\n📊 Summary:')
            personalized_count = assignments.filter(personlized_msg_to_send__gt='').count()
            unpersonalized_count = assignments.filter(personlized_msg_to_send='').count()
            
            self.stdout.write(f'   Personalized: {personalized_count}')
            self.stdout.write(f'   Unpersonalized: {unpersonalized_count}')
            self.stdout.write(f'   Total: {assignments.count()}')
            
            if campaign.start_date is None:
                self.stdout.write('\n💡 Recommendation:')
                self.stdout.write('   Set a start_date for the campaign to avoid AI data issues')
                self.stdout.write(f'   Example: Campaign.objects.filter(id={campaign_id}).update(start_date=timezone.now().date())')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'💥 Error during debugging: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
