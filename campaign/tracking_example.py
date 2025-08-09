"""
Example usage of the email tracking system
"""

# Example 1: Enable tracking for a campaign
def enable_tracking_example():
    """
    Example of how to enable tracking for a campaign
    """
    from campaign.models import Campaign, CampaignOptions
    
    # Get a campaign
    campaign = Campaign.objects.first()
    
    # Get or create campaign options
    options, created = CampaignOptions.objects.get_or_create(
        campaign=campaign,
        defaults={
            'open_tracking_enabled': True,
            'link_tracking_enabled': True,
            'stop_on_reply': True,
        }
    )
    
    if not created:
        # Update existing options
        options.open_tracking_enabled = True
        options.link_tracking_enabled = True
        options.save()
    
    print(f"✅ Tracking enabled for campaign: {campaign.name}")


# Example 2: Manual tracking integration
def manual_tracking_example():
    """
    Example of manually adding tracking to HTML content
    """
    from campaign.tracking import add_tracking_to_email
    from campaign.models import MessageAssignment
    
    # Sample HTML content
    html_content = """
    <html>
    <body>
        <h1>Hello {{first_name}}!</h1>
        <p>Check out our <a href="https://example.com">amazing product</a>!</p>
        <p>Also, <a href="https://newsletter.example.com">subscribe to our newsletter</a>.</p>
    </body>
    </html>
    """
    
    # Get a message assignment
    message_assignment = MessageAssignment.objects.first()
    
    if message_assignment:
        # Add tracking
        tracked_html = add_tracking_to_email(html_content, message_assignment)
        
        print("Original HTML length:", len(html_content))
        print("Tracked HTML length:", len(tracked_html))
        print("Tracking added successfully!")
        
        return tracked_html
    else:
        print("No MessageAssignment found")
        return html_content


# Example 3: Check tracking status
def check_tracking_status():
    """
    Example of checking tracking status for campaigns
    """
    from campaign.models import Campaign, MessageAssignment
    
    print("📊 Tracking Status Report")
    print("=" * 50)
    
    for campaign in Campaign.objects.all()[:5]:  # First 5 campaigns
        options = campaign.campaign_options.first()
        
        if options:
            open_enabled = "✅" if options.open_tracking_enabled else "❌"
            click_enabled = "✅" if options.link_tracking_enabled else "❌"
        else:
            open_enabled = "❓"
            click_enabled = "❓"
        
        # Count opens and clicks
        total_assignments = MessageAssignment.objects.filter(campaign=campaign).count()
        opened_assignments = MessageAssignment.objects.filter(
            campaign=campaign, 
            opened=True
        ).count()
        
        open_rate = (opened_assignments / total_assignments * 100) if total_assignments > 0 else 0
        
        print(f"Campaign: {campaign.name}")
        print(f"  Open Tracking: {open_enabled}")
        print(f"  Click Tracking: {click_enabled}")
        print(f"  Messages Sent: {total_assignments}")
        print(f"  Messages Opened: {opened_assignments}")
        print(f"  Open Rate: {open_rate:.1f}%")
        print()


# Example 4: Custom tracking event handling
def custom_tracking_handler_example():
    """
    Example of how tracking events are handled
    """
    from campaign.models import MessageAssignment, CampaignStats
    from django.utils import timezone
    
    # Simulate an open event
    def handle_open_event(message_assignment_id):
        try:
            assignment = MessageAssignment.objects.get(id=message_assignment_id)
            
            if not assignment.opened:
                # Mark as opened
                assignment.opened = True
                assignment.opened_at = timezone.now()
                assignment.save(update_fields=['opened', 'opened_at'])
                
                # Update campaign stats
                stats, created = CampaignStats.objects.get_or_create(
                    campaign=assignment.campaign,
                    defaults={'opened_count': 0, 'clicked_count': 0}
                )
                stats.opened_count += 1
                stats.save(update_fields=['opened_count'])
                
                print(f"✅ Email opened: Assignment {message_assignment_id}")
            else:
                print(f"📧 Email already opened: Assignment {message_assignment_id}")
                
        except MessageAssignment.DoesNotExist:
            print(f"❌ Assignment {message_assignment_id} not found")
    
    # Example usage
    assignment = MessageAssignment.objects.first()
    if assignment:
        handle_open_event(assignment.id)


# Example 5: Testing tracking URLs
def test_tracking_urls():
    """
    Example of testing tracking URL generation
    """
    from campaign.tracking import get_pytracking_configuration
    
    config = get_pytracking_configuration()
    
    print("🔧 Tracking Configuration:")
    print(f"Open tracking base URL: {config.base_open_tracking_url}")
    print(f"Click tracking base URL: {config.base_click_tracking_url}")
    
    # Test URL generation (this would normally be done by pytracking)
    sample_metadata = {
        'message_assignment_id': 123,
        'campaign_id': 456,
        'lead_id': 789
    }
    
    print(f"\nSample tracking metadata: {sample_metadata}")
    print("✅ Configuration is ready for use")


if __name__ == "__main__":
    print("🚀 Email Tracking Examples")
    print("=" * 50)
    
    # Run examples (uncomment to test)
    # enable_tracking_example()
    # manual_tracking_example()
    # check_tracking_status()
    # custom_tracking_handler_example()
    test_tracking_urls()
