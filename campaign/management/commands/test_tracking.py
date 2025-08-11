"""
Management command to test email tracking functionality
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from campaign.models import Campaign, CampaignOptions, MessageAssignment
from campaign.tracking import get_pytracking_configuration, add_tracking_to_email


class Command(BaseCommand):
    help = 'Test email tracking functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample',
            action='store_true',
            help='Create a sample tracked email HTML file',
        )
        parser.add_argument(
            '--test-config',
            action='store_true',
            help='Test tracking configuration',
        )
        parser.add_argument(
            '--enable-tracking',
            action='store_true',
            help='Enable tracking for the first campaign',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Email Tracking Test Tool')
        )
        
        if options['test_config']:
            self.test_configuration()
        
        if options['enable_tracking']:
            self.enable_tracking()
        
        if options['create_sample']:
            self.create_sample_email()
        
        if not any([options['test_config'], options['enable_tracking'], options['create_sample']]):
            self.show_help()

    def test_configuration(self):
        """Test the tracking configuration"""
        self.stdout.write('\n🔧 Testing Tracking Configuration...')
        
        try:
            # Test Django settings
            pytracking_config = getattr(settings, 'PYTRACKING_CONFIGURATION', None)
            if pytracking_config:
                self.stdout.write(
                    self.style.SUCCESS('✅ PYTRACKING_CONFIGURATION found in Django settings')
                )
                self.stdout.write(f'   Open URL: {pytracking_config.get("base_open_tracking_url")}')
                self.stdout.write(f'   Click URL: {pytracking_config.get("base_click_tracking_url")}')
            else:
                self.stdout.write(
                    self.style.ERROR('❌ PYTRACKING_CONFIGURATION not found in Django settings')
                )
                return
            
            # Test configuration object
            config = get_pytracking_configuration()
            self.stdout.write(
                self.style.SUCCESS('✅ Configuration object created successfully')
            )
            self.stdout.write(f'   Open tracking URL: {config.base_open_tracking_url}')
            self.stdout.write(f'   Click tracking URL: {config.base_click_tracking_url}')
            
            # Check if using ngrok
            if 'ngrok' in config.base_open_tracking_url:
                self.stdout.write(
                    self.style.SUCCESS('✅ Using ngrok URLs - external tracking will work')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️ Not using ngrok URLs - tracking may only work locally')
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Configuration test failed: {str(e)}')
            )

    def enable_tracking(self):
        """Enable tracking for the first campaign"""
        self.stdout.write('\n⚙️ Enabling Tracking...')
        
        try:
            campaign = Campaign.objects.first()
            if not campaign:
                self.stdout.write(
                    self.style.ERROR('❌ No campaigns found. Create a campaign first.')
                )
                return
            
            options, created = CampaignOptions.objects.get_or_create(
                campaign=campaign,
                defaults={
                    'open_tracking_enabled': True,
                    'link_tracking_enabled': True,
                    'stop_on_reply': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created campaign options for "{campaign.name}" with tracking enabled')
                )
            else:
                # Update existing options
                options.open_tracking_enabled = True
                options.link_tracking_enabled = True
                options.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated campaign options for "{campaign.name}" - tracking enabled')
                )
            
            self.stdout.write(f'   Campaign: {campaign.name} (ID: {campaign.id})')
            self.stdout.write(f'   Open tracking: ✅ Enabled')
            self.stdout.write(f'   Click tracking: ✅ Enabled')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to enable tracking: {str(e)}')
            )

    def create_sample_email(self):
        """Create a sample tracked email"""
        self.stdout.write('\n📧 Creating Sample Tracked Email...')
        
        try:
            # Get a message assignment
            message_assignment = MessageAssignment.objects.first()
            if not message_assignment:
                self.stdout.write(
                    self.style.ERROR('❌ No message assignments found. Create a campaign with messages first.')
                )
                return
            
            campaign = message_assignment.campaign
            self.stdout.write(f'Using MessageAssignment ID: {message_assignment.id}')
            self.stdout.write(f'Campaign: {campaign.name}')
            
            # Ensure tracking is enabled
            options = campaign.campaign_options.first()
            if not options or not (options.open_tracking_enabled or options.link_tracking_enabled):
                self.stdout.write(
                    self.style.WARNING('⚠️ Tracking not enabled for this campaign. Run with --enable-tracking first.')
                )
                return
            
            # Create sample HTML
            sample_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Test Email - {campaign.name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                    .header {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 8px; }}
                    .content {{ padding: 20px; }}
                    .cta {{ background: #007cba; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; }}
                    .footer {{ background: #f8f9fa; padding: 15px; font-size: 12px; color: #666; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚀 Test Email with Tracking</h1>
                    <p>Campaign: {campaign.name}</p>
                </div>
                <div class="content">
                    <p>Hello {{{{first_name}}}},</p>
                    <p>This is a test email to verify that our tracking system is working correctly.</p>
                    
                    <h3>Test Links:</h3>
                    <ul>
                        <li><a href="https://example.com/product">Product Page</a> - Test click tracking</li>
                        <li><a href="https://example.com/blog">Blog</a> - Another test link</li>
                        <li><a href="https://google.com">Google</a> - External link test</li>
                    </ul>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="https://example.com/cta" class="cta">🎯 Main Call-to-Action</a>
                    </p>
                    
                    <p>If you can see this email and the links work, then tracking is functioning properly!</p>
                    
                    <p>Best regards,<br>The Development Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent as part of the {campaign.name} campaign.</p>
                    <p>MessageAssignment ID: {message_assignment.id}</p>
                    <p><small>Tracking: Open ({'✅' if options.open_tracking_enabled else '❌'}) | Click ({'✅' if options.link_tracking_enabled else '❌'})</small></p>
                </div>
            </body>
            </html>
            """
            
            # Add tracking
            tracked_html = add_tracking_to_email(sample_html, message_assignment)
            
            # Save to file
            output_file = '/tmp/tracked_email_sample.html'
            with open(output_file, 'w') as f:
                f.write(tracked_html)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Sample email created: {output_file}')
            )
            self.stdout.write(f'📊 Original HTML: {len(sample_html)} characters')
            self.stdout.write(f'📊 Tracked HTML: {len(tracked_html)} characters')
            self.stdout.write(f'📊 Tracking added: {len(tracked_html) - len(sample_html)} characters')
            
            # Analyze tracking elements
            open_pixels = tracked_html.count('<img')
            click_links = tracked_html.count('/campaign/tracking/click/')
            ngrok_urls = tracked_html.count('ngrok')
            
            self.stdout.write(f'📊 Open tracking pixels: {open_pixels}')
            self.stdout.write(f'📊 Click tracking links: {click_links}')
            self.stdout.write(f'📊 ngrok URLs: {ngrok_urls}')
            
            if ngrok_urls > 0:
                self.stdout.write(
                    self.style.SUCCESS('🌐 Email contains ngrok URLs - ready for external testing!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️ No ngrok URLs found - check SITE_URL configuration')
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to create sample email: {str(e)}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())

    def show_help(self):
        """Show usage help"""
        self.stdout.write('\n📖 Usage Examples:')
        self.stdout.write('  Test configuration:')
        self.stdout.write('    python manage.py test_tracking --test-config')
        self.stdout.write('  Enable tracking for first campaign:')
        self.stdout.write('    python manage.py test_tracking --enable-tracking')
        self.stdout.write('  Create sample tracked email:')
        self.stdout.write('    python manage.py test_tracking --create-sample')
        self.stdout.write('  Run all tests:')
        self.stdout.write('    python manage.py test_tracking --test-config --enable-tracking --create-sample')
