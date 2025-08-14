from django.utils import timezone
from django.db.models import F
from .models import Campaign, CampaignStats, CampaignDailyStats, MessageAssignment, CampaignLead
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service class to handle campaign analytics updates efficiently.
    Provides both real-time incremental updates and batch recalculation.
    """
    
    @staticmethod
    def handle_email_sent(message_assignment):
        """
        Handle analytics when an email is sent.
        Uses incremental updates for performance.
        """
        try:
            campaign = message_assignment.campaign
            if not campaign:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Increment sequence_started_count if this is the lead's first sent email
            lead_first_email = not MessageAssignment.objects.filter(
                campaign_lead=message_assignment.campaign_lead,
                sent_at__isnull=False
            ).exclude(id=message_assignment.id).exists()
            
            if lead_first_email:
                # This lead just started the sequence
                stats.sequence_started_count = F('sequence_started_count') + 1
                stats.save(update_fields=['sequence_started_count'])
                
            logger.info(f"Analytics updated for email sent: {message_assignment.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for email sent: {str(e)}")
    
    @staticmethod
    def handle_email_opened(message_assignment):
        """
        Handle analytics when an email is opened.
        Uses incremental updates for performance.
        """
        try:
            campaign = message_assignment.campaign
            if not campaign:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Check if this is the lead's first open
            lead_first_open = not MessageAssignment.objects.filter(
                campaign_lead=message_assignment.campaign_lead,
                opened=True
            ).exclude(id=message_assignment.id).exists()
            
            if lead_first_open:
                # This lead just opened their first email
                stats.opened_count = F('opened_count') + 1
                stats.save(update_fields=['opened_count'])
                
            logger.info(f"Analytics updated for email opened: {message_assignment.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for email opened: {str(e)}")
    
    @staticmethod
    def handle_link_clicked(link):
        """
        Handle analytics when a link is clicked.
        Uses incremental updates for performance.
        """
        try:
            campaign = link.campaign
            campaign_lead = link.campaign_lead
            
            if not campaign or not campaign_lead:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Check if this is the lead's first click on any link
            lead_first_click = not MessageAssignment.objects.filter(
                campaign_lead=campaign_lead,
                url__visit_count__gt=0
            ).exists() and not MessageAssignment.objects.filter(
                campaign_lead=campaign_lead,
                newsletter_link__visit_count__gt=0
            ).exists()
            
            if lead_first_click:
                # This lead just clicked their first link
                stats.clicked_count = F('clicked_count') + 1
                stats.save(update_fields=['clicked_count'])
                
            logger.info(f"Analytics updated for link clicked: {link.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for link clicked: {str(e)}")
    
    @staticmethod
    def handle_email_replied(message_assignment):
        """
        Handle analytics when an email is replied to.
        Also triggers automatic opportunity marking.
        """
        try:
            campaign = message_assignment.campaign
            campaign_lead = message_assignment.campaign_lead
            
            if not campaign or not campaign_lead:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Check if this is the lead's first reply
            lead_first_reply = not MessageAssignment.objects.filter(
                campaign_lead=campaign_lead,
                responded=True
            ).exclude(id=message_assignment.id).exists()
            
            if lead_first_reply:
                # This lead just replied for the first time
                stats.replied_count = F('replied_count') + 1
                
                # Auto-mark as opportunity (your requirement)
                if campaign_lead.opportunity_status == 'none':
                    campaign_lead.mark_as_opportunity()
                    # This will trigger opportunity count update via the model method
                else:
                    # Just update reply count
                    stats.save(update_fields=['replied_count'])
                
            logger.info(f"Analytics updated for email replied: {message_assignment.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for email replied: {str(e)}")
    
    @staticmethod
    def handle_opportunity_marked(campaign_lead):
        """
        Handle analytics when a lead is marked as opportunity.
        """
        try:
            campaign = campaign_lead.campaign
            if not campaign:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Increment opportunity count and value
            stats.opportunities_count += 1
            
            stats.save(update_fields=['opportunities_count'])
            
            logger.info(f"Analytics updated for opportunity marked: {campaign_lead.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for opportunity marked: {str(e)}")
    
    @staticmethod
    def handle_conversion_marked(campaign_lead):
        """
        Handle analytics when a lead is converted.
        """
        try:
            campaign = campaign_lead.campaign
            if not campaign:
                return
            
            # Get or create campaign stats
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            
            # Increment conversion count and value
            stats.conversions_count = F('conversions_count') + 1
            if campaign_lead.conversion_value:
                stats.conversions_total_value = F('conversions_total_value') + campaign_lead.conversion_value
            
            stats.save(update_fields=['conversions_count', 'conversions_total_value'])
            
            logger.info(f"Analytics updated for conversion marked: {campaign_lead.id}")
            
        except Exception as e:
            logger.error(f"Error updating analytics for conversion marked: {str(e)}")
    
    @staticmethod
    def recalculate_campaign_stats(campaign):
        """
        Full recalculation of campaign stats.
        Use this for:
        - Initial setup
        - Data corrections
        - Periodic verification
        """
        try:
            stats, created = CampaignStats.objects.get_or_create(campaign=campaign)
            stats.update_from_campaign()
            
            logger.info(f"Full analytics recalculation completed for campaign: {campaign.id}")
            
        except Exception as e:
            logger.error(f"Error in full analytics recalculation: {str(e)}")
    
    @staticmethod
    def batch_update_campaigns(campaign_ids=None):
        """
        Batch update multiple campaigns.
        Use this for:
        - End of day reconciliation
        - Periodic maintenance
        """
        try:
            if campaign_ids:
                campaigns = Campaign.objects.filter(id__in=campaign_ids)
            else:
                campaigns = Campaign.objects.filter(status='active')
            
            for campaign in campaigns:
                AnalyticsService.recalculate_campaign_stats(campaign)
            
            logger.info(f"Batch analytics update completed for {campaigns.count()} campaigns")
            
        except Exception as e:
            logger.error(f"Error in batch analytics update: {str(e)}")


class DailyStatsService:
    """
    Service for handling daily stats calculations.
    """
    
    @staticmethod
    def calculate_daily_stats_for_campaign(campaign, target_date=None):
        """
        Calculate daily stats for a specific campaign.
        This is called by the Celery task.
        """
        return CampaignDailyStats.calculate_daily_stats(campaign, target_date)
    
    @staticmethod
    def schedule_daily_stats_calculation():
        """
        Schedule daily stats calculation for all active campaigns.
        Call this from Inngest or Celery Beat.
        """
        from .tasks import calculate_all_campaigns_daily_stats_task
        calculate_all_campaigns_daily_stats_task.delay()
