"""
Test script for email tracking functionality
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/omar/Desktop/cccrm')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from campaign.models import MessageAssignment, Campaign, CampaignOptions
from campaign.tracking import add_tracking_to_email, get_pytracking_configuration


def test_tracking_configuration():
    """Test pytracking configuration"""
    print("🔧 Testing pytracking configuration...")
    
    try:
        config = get_pytracking_configuration()
        print(f"✅ Base open tracking URL: {config.base_open_tracking_url}")
        print(f"✅ Base click tracking URL: {config.base_click_tracking_url}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False


def test_html_tracking():
    """Test HTML tracking modification"""
    print("\n📧 Testing HTML tracking modification...")
    
    # Sample HTML content
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Test Email</title>
    </head>
    <body>
        <h1>Hello World!</h1>
        <p>This is a test email with a <a href="https://example.com">link</a>.</p>
        <p>And another <a href="https://google.com">link to Google</a>.</p>
    </body>
    </html>
    """
    
    try:
        # Get a sample message assignment (if available)
        message_assignment = MessageAssignment.objects.first()
        
        if not message_assignment:
            print("❌ No MessageAssignment found in database")
            return False
            
        print(f"✅ Using MessageAssignment ID: {message_assignment.id}")
        
        # Test tracking modification
        tracked_html = add_tracking_to_email(sample_html, message_assignment)
        
        print(f"📏 Original HTML length: {len(sample_html)}")
        print(f"📏 Tracked HTML length: {len(tracked_html)}")
        
        # Check if tracking was added
        if len(tracked_html) > len(sample_html):
            print("✅ Tracking appears to have been added (HTML length increased)")
            
            # Look for tracking indicators
            if 'tracking' in tracked_html.lower():
                print("✅ Found 'tracking' in modified HTML")
            
            # Save sample for inspection
            with open('/tmp/tracked_email_sample.html', 'w') as f:
                f.write(tracked_html)
            print("✅ Saved tracked HTML sample to /tmp/tracked_email_sample.html")
            
            return True
        else:
            print("⚠️ HTML length unchanged - tracking may not be enabled")
            return False
            
    except Exception as e:
        print(f"❌ HTML tracking test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_campaign_options():
    """Test campaign options for tracking"""
    print("\n⚙️ Testing campaign options...")
    
    try:
        campaigns_with_options = Campaign.objects.filter(campaign_options__isnull=False)
        
        if not campaigns_with_options.exists():
            print("❌ No campaigns with options found")
            return False
            
        for campaign in campaigns_with_options[:3]:  # Test first 3
            options = campaign.campaign_options.first()
            print(f"📊 Campaign: {campaign.name}")
            print(f"   Open tracking: {options.open_tracking_enabled}")
            print(f"   Link tracking: {options.link_tracking_enabled}")
            
        return True
        
    except Exception as e:
        print(f"❌ Campaign options test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("🚀 Starting email tracking tests...\n")
    
    tests = [
        ("Configuration", test_tracking_configuration),
        ("Campaign Options", test_campaign_options),
        ("HTML Tracking", test_html_tracking),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test")
        print('='*50)
        
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Email tracking is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")


if __name__ == "__main__":
    main()
