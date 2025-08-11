"""
Test script to verify pytracking configuration fix
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/omar/Desktop/cccrm')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from django.conf import settings
from campaign.tracking import get_pytracking_configuration, add_tracking_to_email, CustomOpenTrackingView, CustomClickTrackingView
from campaign.models import MessageAssignment, Campaign, CampaignOptions


def test_django_settings():
    """Test Django settings configuration"""
    print("🔧 Testing Django Settings...")
    
    try:
        pytracking_config = getattr(settings, 'PYTRACKING_CONFIGURATION', None)
        if pytracking_config:
            print("✅ PYTRACKING_CONFIGURATION found in settings")
            print(f"   Open URL: {pytracking_config.get('base_open_tracking_url')}")
            print(f"   Click URL: {pytracking_config.get('base_click_tracking_url')}")
            return True
        else:
            print("❌ PYTRACKING_CONFIGURATION not found in settings")
            return False
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False


def test_configuration_object():
    """Test configuration object creation"""
    print("\n🔧 Testing Configuration Object...")
    
    try:
        config = get_pytracking_configuration()
        print(f"✅ Configuration created successfully")
        print(f"   Open URL: {config.base_open_tracking_url}")
        print(f"   Click URL: {config.base_click_tracking_url}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_view_configuration():
    """Test that views can get configuration"""
    print("\n🔧 Testing View Configuration...")
    
    try:
        # Test open tracking view
        open_view = CustomOpenTrackingView()
        open_config = open_view.get_configuration()
        print(f"✅ Open view configuration: {open_config.base_open_tracking_url}")
        
        # Test click tracking view
        click_view = CustomClickTrackingView()
        click_config = click_view.get_configuration()
        print(f"✅ Click view configuration: {click_config.base_click_tracking_url}")
        
        return True
    except Exception as e:
        print(f"❌ View configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_html_adaptation():
    """Test HTML adaptation with tracking"""
    print("\n📧 Testing HTML Adaptation...")
    
    try:
        # Get a message assignment
        message_assignment = MessageAssignment.objects.first()
        if not message_assignment:
            print("❌ No message assignments found")
            return False
        
        # Ensure campaign has tracking enabled
        campaign = message_assignment.campaign
        options, created = CampaignOptions.objects.get_or_create(
            campaign=campaign,
            defaults={
                'open_tracking_enabled': True,
                'link_tracking_enabled': True,
            }
        )
        
        if not options.open_tracking_enabled or not options.link_tracking_enabled:
            options.open_tracking_enabled = True
            options.link_tracking_enabled = True
            options.save()
            print("✅ Enabled tracking for campaign")
        
        # Test HTML
        sample_html = """
        <html>
        <body>
            <h1>Test Email</h1>
            <p>Visit our <a href="https://example.com">website</a>!</p>
            <p>Also check our <a href="https://blog.example.com">blog</a>.</p>
        </body>
        </html>
        """
        
        print(f"📏 Original HTML length: {len(sample_html)}")
        
        tracked_html = add_tracking_to_email(sample_html, message_assignment)
        print(f"📏 Tracked HTML length: {len(tracked_html)}")
        
        if len(tracked_html) > len(sample_html):
            print("✅ Tracking added successfully")
            
            # Check for tracking elements
            if '<img' in tracked_html and 'tracking/open/' in tracked_html:
                print("✅ Open tracking pixel found")
            else:
                print("❌ Open tracking pixel not found")
            
            if 'tracking/click/' in tracked_html:
                print("✅ Click tracking URLs found")
            else:
                print("❌ Click tracking URLs not found")
            
            # Check for ngrok URLs
            if 'ngrok' in tracked_html:
                print("✅ ngrok URLs found in tracking")
            else:
                print("⚠️ No ngrok URLs found")
            
            # Save sample
            with open('/tmp/pytracking_test_sample.html', 'w') as f:
                f.write(tracked_html)
            print("💾 Saved sample to /tmp/pytracking_test_sample.html")
            
            return True
        else:
            print("❌ No tracking added")
            return False
            
    except Exception as e:
        print(f"❌ HTML adaptation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_url_generation():
    """Test URL generation manually"""
    print("\n🔗 Testing URL Generation...")
    
    try:
        from pytracking.html import adapt_html
        from campaign.tracking import get_pytracking_configuration
        
        config = get_pytracking_configuration()
        
        sample_html = '<p>Test <a href="https://example.com">link</a></p>'
        metadata = {'test': 'data'}
        
        tracked_html = adapt_html(
            sample_html,
            extra_metadata=metadata,
            configuration=config,
            open_tracking=True,
            click_tracking=True
        )
        
        print(f"✅ URL generation test successful")
        print(f"📏 Original: {len(sample_html)} chars")
        print(f"📏 Tracked: {len(tracked_html)} chars")
        
        if 'ngrok' in tracked_html:
            print("✅ ngrok URLs generated correctly")
        else:
            print("⚠️ No ngrok URLs in generated HTML")
        
        return True
        
    except Exception as e:
        print(f"❌ URL generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Testing PyTracking Configuration Fix\n")
    
    tests = [
        ("Django Settings", test_django_settings),
        ("Configuration Object", test_configuration_object),
        ("View Configuration", test_view_configuration),
        ("HTML Adaptation", test_html_adaptation),
        ("URL Generation", test_url_generation),
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
        print("🎉 All tests passed! PyTracking should now work correctly.")
        print("\n📋 Next steps:")
        print("1. Send a test email")
        print("2. Check if tracking URLs work")
        print("3. Monitor Django logs for tracking events")
    else:
        print("⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
