"""
Management command to enable email tracking for existing campaigns
"""
from django.core.management.base import BaseCommand
from campaign.models import Campaign, CampaignOptions


class Command(BaseCommand):
    help = 'Enable email tracking for existing campaigns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--campaign-id',
            type=int,
            help='Enable tracking for a specific campaign ID',
        )
        parser.add_argument(
            '--open-tracking',
            action='store_true',
            help='Enable open tracking',
        )
        parser.add_argument(
            '--click-tracking',
            action='store_true',
            help='Enable click tracking',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Enable tracking for all campaigns',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Email Tracking Configuration Tool')
        )
        
        # Determine which campaigns to update
        if options['campaign_id']:
            campaigns = Campaign.objects.filter(id=options['campaign_id'])
            if not campaigns.exists():
                self.stdout.write(
                    self.style.ERROR(f'❌ Campaign with ID {options["campaign_id"]} not found')
                )
                return
        elif options['all']:
            campaigns = Campaign.objects.all()
        else:
            # Interactive mode - show available campaigns
            self.show_campaigns()
            return

        # Determine what tracking to enable
        enable_open = options['open_tracking']
        enable_click = options['click_tracking']
        
        if not enable_open and not enable_click:
            # Default: enable both
            enable_open = True
            enable_click = True
            self.stdout.write(
                self.style.WARNING('⚠️ No specific tracking type specified, enabling both open and click tracking')
            )

        # Process campaigns
        updated_count = 0
        created_count = 0
        
        for campaign in campaigns:
            self.stdout.write(f'\n📊 Processing campaign: {campaign.name} (ID: {campaign.id})')
            
            # Get or create campaign options
            options_obj, created = CampaignOptions.objects.get_or_create(
                campaign=campaign,
                defaults={
                    'open_tracking_enabled': enable_open,
                    'link_tracking_enabled': enable_click,
                    'stop_on_reply': True,
                    'send_as_text_only': False,
                    'send_first_email_as_text_only': False,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Created new campaign options with tracking enabled')
                )
            else:
                # Update existing options
                changed = False
                
                if options_obj.open_tracking_enabled != enable_open:
                    if not options['dry_run']:
                        options_obj.open_tracking_enabled = enable_open
                    changed = True
                    status = "enabled" if enable_open else "disabled"
                    self.stdout.write(f'   📧 Open tracking: {status}')
                
                if options_obj.link_tracking_enabled != enable_click:
                    if not options['dry_run']:
                        options_obj.link_tracking_enabled = enable_click
                    changed = True
                    status = "enabled" if enable_click else "disabled"
                    self.stdout.write(f'   🔗 Click tracking: {status}')
                
                if changed:
                    if not options['dry_run']:
                        options_obj.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'   ✅ Updated campaign options')
                    )
                else:
                    self.stdout.write(f'   ℹ️ No changes needed')

        # Summary
        self.stdout.write(f'\n{"="*50}')
        self.stdout.write(self.style.SUCCESS('📊 SUMMARY'))
        self.stdout.write(f'{"="*50}')
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN - No changes were made'))
        
        self.stdout.write(f'📈 Campaigns processed: {campaigns.count()}')
        self.stdout.write(f'🆕 New campaign options created: {created_count}')
        self.stdout.write(f'🔄 Existing campaign options updated: {updated_count}')
        
        if enable_open:
            self.stdout.write(f'📧 Open tracking: ENABLED')
        if enable_click:
            self.stdout.write(f'🔗 Click tracking: ENABLED')

    def show_campaigns(self):
        """Show available campaigns and usage instructions"""
        campaigns = Campaign.objects.all()
        
        if not campaigns.exists():
            self.stdout.write(
                self.style.ERROR('❌ No campaigns found in the database')
            )
            return
        
        self.stdout.write('\n📋 Available campaigns:')
        self.stdout.write('-' * 50)
        
        for campaign in campaigns[:10]:  # Show first 10
            options = campaign.campaign_options.first()
            if options:
                open_status = "✅" if options.open_tracking_enabled else "❌"
                click_status = "✅" if options.link_tracking_enabled else "❌"
                tracking_info = f"Open: {open_status} Click: {click_status}"
            else:
                tracking_info = "No options configured"
            
            self.stdout.write(f'ID: {campaign.id:3d} | {campaign.name[:30]:30s} | {tracking_info}')
        
        if campaigns.count() > 10:
            self.stdout.write(f'... and {campaigns.count() - 10} more campaigns')
        
        self.stdout.write('\n📖 Usage examples:')
        self.stdout.write('  Enable tracking for all campaigns:')
        self.stdout.write('    python manage.py enable_tracking --all')
        self.stdout.write('  Enable tracking for specific campaign:')
        self.stdout.write('    python manage.py enable_tracking --campaign-id 1')
        self.stdout.write('  Enable only open tracking:')
        self.stdout.write('    python manage.py enable_tracking --all --open-tracking')
        self.stdout.write('  Dry run (preview changes):')
        self.stdout.write('    python manage.py enable_tracking --all --dry-run')
