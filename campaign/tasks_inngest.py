# Inngest functions for campaign processing
import inngest
from scheduler.client import inngest_client

from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta
from .models import MessageAssignment
from .services import AnalyticsService

logger = logging.getLogger(__name__)


# COMMENTED OUT - Using batch processing instead of individual message processing
# @inngest_client.create_function(
#     fn_id="personalize_message",
#     trigger=inngest.TriggerEvent(event="campaigns/personalize.message"),
# )
# def personalize_message_task(ctx: inngest.Context):
#     """
#     Inngest function to personalize a message using AI and save it to the database.
#     Rate limited to respect AI API limits.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass






# COMMENTED OUT - Using batch processing instead of individual campaign message processing
# @inngest_client.create_function(
#     fn_id="personalize_campaign_messages",
#     trigger=inngest.TriggerEvent(event="campaigns/personalize.campaign_messages"),
# )
# def personalize_campaign_messages_task(ctx: inngest.Context):
#     """
#     Inngest function to personalize all messages for a campaign.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass















# COMMENTED OUT - Using batch processing instead of individual email sending
# @inngest_client.create_function(
#     fn_id="send_email",
#     trigger=inngest.TriggerEvent(event="campaigns/send.email"),
# )
# def send_email_task(ctx: inngest.Context):
#     """
#     Inngest function to send an email for a message assignment.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass



















# COMMENTED OUT - Using batch processing instead of individual campaign email sending
# @inngest_client.create_function(
#     fn_id="send_campaign_emails",
#     trigger=inngest.TriggerEvent(event="campaigns/send.campaign_emails"),
# )
# def send_campaign_emails_task(ctx: inngest.Context):
#     """
#     Inngest function to send emails for all message assignments in a campaign.
#
#     DEPRECATED: Now using batch processing in personalize_and_send_all_emails_at_once
#     """
#     pass











@inngest_client.create_function(
    fn_id="personalize_and_send_all_emails",
    trigger=inngest.TriggerEvent(event="campaigns/personalize_and_send.all_emails"),
)
def personalize_and_send_all_emails_at_once(ctx: inngest.Context):
    """
    Inngest function to personalize and send all emails at once for a specific campaign.
    This function processes everything in batches to avoid creating too many individual events.

    Args:
        ctx.event.data.campaign_id: ID of the Campaign

    Returns:
        dict: Results of the operation
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            error_msg = f"Campaign with ID {campaign_id} not found"
            return {
                'status': 'error',
                'message': error_msg,
                'campaign_id': campaign_id
            }

        logger.info(f"🚀 Starting campaign launch for {campaign.name} (ID: {campaign_id})")

        # Step 1: Personalize all messages that need personalization
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            personlized_msg_to_send=''
        )

        personalize_count = query.count()
        logger.info(f"📝 Personalizing {personalize_count} messages")

        for message_assignment in query:
            success = message_assignment.personalize_with_ai(skip=True)
            if success:
                logger.info(f"✅ Personalized message for assignment ID {message_assignment.id}")
            else:
                logger.error(f"❌ Failed to personalize message for assignment ID {message_assignment.id}")

        # Step 2: Send all personalized emails
        send_query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False,
            personlized_msg_to_send__gt=''
        )

        send_count = send_query.count()
        logger.info(f"📧 Sending {send_count} emails")

        from campaign.email_sender import send_campaign_email
        sent_successfully = 0

        for message_assignment in send_query:
            try:
                success = send_campaign_email(message_assignment, campaign)
                if success:
                    sent_successfully += 1
                    logger.info(f"✅ Email sent successfully to {message_assignment.campaign_lead.lead.email}")
                else:
                    logger.error(f"❌ Failed to send email to {message_assignment.campaign_lead.lead.email}")
            except Exception as e:
                logger.error(f"💥 Error sending email to {message_assignment.campaign_lead.lead.email}: {str(e)}")

        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch completed successfully',
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'personalized_count': personalize_count,
            'sent_count': sent_successfully,
            'total_processed': send_count
        }

    except Exception as e:
        logger.error(f"Error launching campaign {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }












# Helper function for backward compatibility
def personalize_and_send_all_emails_at_once_sync(campaign_id):
    """
    Synchronous helper function to trigger the Inngest function.
    Used for backward compatibility with existing code.
    """
    try:
        inngest_client.send_sync(
            inngest.Event(
                name="campaigns/personalize_and_send.all_emails",
                data={"campaign_id": campaign_id}
            )
        )
        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch initiated successfully',
            'campaign_id': campaign_id
        }
    except Exception as e:
        logger.error(f"Error triggering campaign launch {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }
