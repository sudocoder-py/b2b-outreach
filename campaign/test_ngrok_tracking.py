"""
Test script specifically for ngrok tracking setup
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/omar/Desktop/cccrm')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from django.conf import settings
from campaign.tracking import get_pytracking_configuration, add_tracking_to_email
from campaign.models import MessageAssignment, Campaign, CampaignOptions


def test_ngrok_configuration():
    """Test that tracking URLs use ngrok domain"""
    print("🌐 Testing ngrok configuration...")
    
    try:
        # Check Django settings
        site_url = getattr(settings, 'SITE_URL', 'Not configured')
        print(f"📋 SITE_URL from settings: {site_url}")
        
        # Check if it's using ngrok
        if 'ngrok' in site_url:
            print("✅ Using ngrok URL")
        else:
            print("⚠️ Not using ngrok URL - tracking may not work from external email clients")
        
        # Get tracking configuration
        config = get_pytracking_configuration()
        print(f"📧 Open tracking URL: {config.base_open_tracking_url}")
        print(f"🔗 Click tracking URL: {config.base_click_tracking_url}")
        
        # Verify URLs use the correct domain
        if 'ngrok' in config.base_open_tracking_url:
            print("✅ Open tracking URLs will use ngrok domain")
        else:
            print("❌ Open tracking URLs not using ngrok domain")
            
        if 'ngrok' in config.base_click_tracking_url:
            print("✅ Click tracking URLs will use ngrok domain")
        else:
            print("❌ Click tracking URLs not using ngrok domain")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False


def test_sample_email_tracking():
    """Test tracking with a sample email"""
    print("\n📧 Testing sample email tracking...")
    
    try:
        # Get or create a test message assignment
        campaign = Campaign.objects.first()
        if not campaign:
            print("❌ No campaigns found - create a campaign first")
            return False
            
        message_assignment = MessageAssignment.objects.filter(campaign=campaign).first()
        if not message_assignment:
            print("❌ No message assignments found - create a message assignment first")
            return False
            
        print(f"✅ Using MessageAssignment ID: {message_assignment.id}")
        print(f"✅ Campaign: {campaign.name}")
        
        # Check campaign options
        options = campaign.campaign_options.first()
        if not options:
            print("⚠️ No campaign options found - creating default options...")
            options = CampaignOptions.objects.create(
                campaign=campaign,
                open_tracking_enabled=True,
                link_tracking_enabled=True
            )
            print("✅ Created campaign options with tracking enabled")
        else:
            print(f"📊 Open tracking enabled: {options.open_tracking_enabled}")
            print(f"📊 Click tracking enabled: {options.link_tracking_enabled}")
        
        # Sample HTML with links
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Test Email</title>
        </head>
        <body>
            <h1>Hello from your email campaign!</h1>
            <p>This is a test email with tracking.</p>
            <p>Check out our <a href="https://example.com/product">amazing product</a>!</p>
            <p>Also visit our <a href="https://example.com/blog">blog</a> for more info.</p>
            <p>Best regards,<br>Your Team</p>
        </body>
        </html>
        """
        
        print(f"📏 Original HTML length: {len(sample_html)}")
        
        # Add tracking
        tracked_html = add_tracking_to_email(sample_html, message_assignment)
        print(f"📏 Tracked HTML length: {len(tracked_html)}")
        
        # Check if tracking was added
        if len(tracked_html) > len(sample_html):
            print("✅ Tracking appears to have been added")
            
            # Look for ngrok URLs in the tracked HTML
            if 'ngrok' in tracked_html:
                print("✅ Found ngrok URLs in tracked HTML")
                
                # Count tracking elements
                open_pixels = tracked_html.count('img')
                modified_links = tracked_html.count('/campaign/tracking/click/')
                
                print(f"📊 Tracking pixels found: {open_pixels}")
                print(f"📊 Modified links found: {modified_links}")
                
            else:
                print("⚠️ No ngrok URLs found in tracked HTML")
            
            # Save sample for inspection
            output_file = '/tmp/ngrok_tracked_email.html'
            with open(output_file, 'w') as f:
                f.write(tracked_html)
            print(f"💾 Saved tracked HTML to: {output_file}")
            
            return True
        else:
            print("❌ No tracking added - check campaign options")
            return False
            
    except Exception as e:
        print(f"❌ Email tracking test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tracking_urls_accessibility():
    """Test if tracking URLs are accessible"""
    print("\n🌐 Testing tracking URL accessibility...")
    
    try:
        import requests
        from django.conf import settings
        
        site_url = getattr(settings, 'SITE_URL', '')
        if not site_url:
            print("❌ SITE_URL not configured")
            return False
            
        # Test if the base URL is accessible
        try:
            response = requests.get(site_url, timeout=10)
            print(f"✅ Base URL accessible: {site_url} (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"❌ Base URL not accessible: {site_url} - {str(e)}")
            return False
            
        # Test tracking endpoints (these will return 404 without proper tracking data, but should not error)
        tracking_urls = [
            f"{site_url}/campaign/tracking/open/test",
            f"{site_url}/campaign/tracking/click/test"
        ]
        
        for url in tracking_urls:
            try:
                response = requests.get(url, timeout=5)
                print(f"📡 Tracking endpoint reachable: {url} (Status: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"❌ Tracking endpoint not reachable: {url} - {str(e)}")
                
        return True
        
    except ImportError:
        print("⚠️ requests library not available - skipping URL accessibility test")
        print("   Install with: pip install requests")
        return True
    except Exception as e:
        print(f"❌ URL accessibility test failed: {str(e)}")
        return False


def main():
    """Run all ngrok-specific tests"""
    print("🚀 Testing Email Tracking with ngrok\n")
    
    tests = [
        ("ngrok Configuration", test_ngrok_configuration),
        ("Sample Email Tracking", test_sample_email_tracking),
        ("URL Accessibility", test_tracking_urls_accessibility),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running {test_name} Test")
        print('='*60)
        
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Email tracking with ngrok is ready!")
        print("\n📋 Next steps:")
        print("1. Send a test email to yourself")
        print("2. Check if the tracking pixel loads (check network tab in email client)")
        print("3. Click links in the email to test click tracking")
        print("4. Check Django admin for updated MessageAssignment.opened and Link.visit_count")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")


if __name__ == "__main__":
    main()
