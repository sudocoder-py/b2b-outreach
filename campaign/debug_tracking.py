"""
Debug utilities for email tracking
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/omar/Desktop/cccrm')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from django.conf import settings
from campaign.models import MessageAssignment, Campaign, CampaignOptions
from campaign.tracking import add_tracking_to_email, get_pytracking_configuration


def debug_tracking_setup():
    """Debug the tracking setup"""
    print("🔍 DEBUGGING EMAIL TRACKING SETUP")
    print("=" * 60)
    
    # 1. Check Django settings
    print("\n1. 📋 Django Settings:")
    print(f"   SITE_URL: {getattr(settings, 'SITE_URL', 'NOT SET')}")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # 2. Check pytracking configuration
    print("\n2. 🔧 PyTracking Configuration:")
    try:
        config = get_pytracking_configuration()
        print(f"   ✅ Open tracking URL: {config.base_open_tracking_url}")
        print(f"   ✅ Click tracking URL: {config.base_click_tracking_url}")
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
    
    # 3. Check campaigns and options
    print("\n3. 📊 Campaign Options:")
    campaigns = Campaign.objects.all()[:5]  # First 5 campaigns
    
    if not campaigns:
        print("   ❌ No campaigns found")
        return
    
    for campaign in campaigns:
        options = campaign.campaign_options.first()
        print(f"   Campaign: {campaign.name} (ID: {campaign.id})")
        
        if options:
            print(f"     Open tracking: {'✅' if options.open_tracking_enabled else '❌'}")
            print(f"     Click tracking: {'✅' if options.link_tracking_enabled else '❌'}")
        else:
            print("     ❌ No campaign options found")
    
    # 4. Test HTML modification
    print("\n4. 📧 HTML Modification Test:")
    message_assignment = MessageAssignment.objects.first()
    
    if not message_assignment:
        print("   ❌ No message assignments found")
        return
    
    print(f"   Using MessageAssignment ID: {message_assignment.id}")
    
    sample_html = """
    <html>
    <body>
        <h1>Test Email</h1>
        <p>Visit our <a href="https://example.com">website</a>!</p>
    </body>
    </html>
    """
    
    try:
        tracked_html = add_tracking_to_email(sample_html, message_assignment)
        
        print(f"   Original length: {len(sample_html)}")
        print(f"   Tracked length: {len(tracked_html)}")
        
        if len(tracked_html) > len(sample_html):
            print("   ✅ Tracking added successfully")
            
            # Check for tracking elements
            if '<img' in tracked_html:
                print("   ✅ Open tracking pixel found")
            else:
                print("   ❌ No open tracking pixel found")
                
            if '/campaign/tracking/click/' in tracked_html:
                print("   ✅ Click tracking URLs found")
            else:
                print("   ❌ No click tracking URLs found")
                
            # Check for ngrok URLs
            if 'ngrok' in tracked_html:
                print("   ✅ ngrok URLs found in tracking")
            else:
                print("   ⚠️ No ngrok URLs found - may not work externally")
                
        else:
            print("   ❌ No tracking added")
            
    except Exception as e:
        print(f"   ❌ HTML modification failed: {e}")
        import traceback
        traceback.print_exc()


def create_test_email_sample():
    """Create a test email sample with tracking"""
    print("\n🧪 CREATING TEST EMAIL SAMPLE")
    print("=" * 60)
    
    try:
        # Get a message assignment
        message_assignment = MessageAssignment.objects.first()
        if not message_assignment:
            print("❌ No message assignments found")
            return
        
        # Ensure campaign has tracking enabled
        campaign = message_assignment.campaign
        options, created = CampaignOptions.objects.get_or_create(
            campaign=campaign,
            defaults={
                'open_tracking_enabled': True,
                'link_tracking_enabled': True,
                'stop_on_reply': True,
            }
        )
        
        if created:
            print(f"✅ Created campaign options for {campaign.name}")
        else:
            # Update to enable tracking
            options.open_tracking_enabled = True
            options.link_tracking_enabled = True
            options.save()
            print(f"✅ Updated campaign options for {campaign.name}")
        
        # Create sample email HTML
        sample_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Test Email - {campaign.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #f4f4f4; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .cta {{ background: #007cba; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; }}
                .footer {{ background: #f4f4f4; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to {campaign.name}!</h1>
                </div>
                <div class="content">
                    <p>Hello {{{{first_name}}}},</p>
                    <p>We're excited to share our latest updates with you!</p>
                    <p>Here are some great resources:</p>
                    <ul>
                        <li><a href="https://example.com/product">Our Amazing Product</a></li>
                        <li><a href="https://example.com/blog">Latest Blog Posts</a></li>
                        <li><a href="https://example.com/support">Customer Support</a></li>
                    </ul>
                    <p style="text-align: center;">
                        <a href="https://example.com/cta" class="cta">Get Started Now</a>
                    </p>
                    <p>Best regards,<br>The Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent as part of the {campaign.name} campaign.</p>
                    <p><a href="https://example.com/unsubscribe">Unsubscribe</a> | <a href="https://example.com/preferences">Email Preferences</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Add tracking
        tracked_html = add_tracking_to_email(sample_html, message_assignment)
        
        # Save to file
        output_file = '/tmp/test_email_with_tracking.html'
        with open(output_file, 'w') as f:
            f.write(tracked_html)
        
        print(f"✅ Test email created: {output_file}")
        print(f"📊 Original HTML: {len(sample_html)} characters")
        print(f"📊 Tracked HTML: {len(tracked_html)} characters")
        print(f"📊 Tracking added: {len(tracked_html) - len(sample_html)} characters")
        
        # Analyze tracking elements
        open_pixels = tracked_html.count('<img')
        click_links = tracked_html.count('/campaign/tracking/click/')
        ngrok_urls = tracked_html.count('ngrok')
        
        print(f"📊 Open tracking pixels: {open_pixels}")
        print(f"📊 Click tracking links: {click_links}")
        print(f"📊 ngrok URLs: {ngrok_urls}")
        
        if ngrok_urls > 0:
            print("✅ Email is ready for external testing with ngrok!")
        else:
            print("⚠️ No ngrok URLs found - check SITE_URL configuration")
            
        return output_file
        
    except Exception as e:
        print(f"❌ Failed to create test email: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all debug functions"""
    debug_tracking_setup()
    create_test_email_sample()
    
    print(f"\n{'='*60}")
    print("🎯 NEXT STEPS")
    print('='*60)
    print("1. Check the generated test email file")
    print("2. Send a test email to yourself")
    print("3. Open the email and check browser network tab")
    print("4. Click links in the email")
    print("5. Check Django admin for tracking updates")
    print("6. Visit /campaign/tracking/test/ to verify endpoints")


if __name__ == "__main__":
    main()
