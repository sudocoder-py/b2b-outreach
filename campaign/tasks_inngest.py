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


@inngest_client.create_function(
    fn_id="personalize_message",
    trigger=inngest.TriggerEvent(event="campaigns/personalize.message"),
)
def personalize_message_task(ctx: inngest.Context):
    """
    Inngest function to personalize a message using AI and save it to the database.
    Rate limited to respect AI API limits.

    Args:
        ctx.event.data.message_assignment_id: ID of the MessageAssignment to personalize
        ctx.event.data.skip: If True, skip AI and use simple replacement

    Returns:
        dict: Result of the operation
    """
    try:
        message_assignment_id = ctx.event.data.get("message_assignment_id")
        skip = ctx.event.data.get("skip", True)

        if not message_assignment_id:
            return {"status": "error", "message": "message_assignment_id is required"}

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)

        success = message_assignment.personalize_with_ai(skip=skip)

        if success:
            logger.info(f"✅ Successfully personalized message for assignment ID {message_assignment_id}")
            return {"status": "success", "message_assignment_id": message_assignment_id}
        else:
            return {"status": "error", "message": "Failed to personalize message", "message_assignment_id": message_assignment_id}

    except MessageAssignment.DoesNotExist:
        return {"status": "error", "message": "MessageAssignment not found", "message_assignment_id": message_assignment_id}
    except Exception as e:
        logger.error(f"Error personalizing message {message_assignment_id}: {str(e)}")
        return {"status": "error", "message": str(e), "message_assignment_id": message_assignment_id}






@inngest_client.create_function(
    fn_id="personalize_campaign_messages",
    trigger=inngest.TriggerEvent(event="campaigns/personalize.campaign_messages"),
)
def personalize_campaign_messages_task(ctx: inngest.Context):
    """
    Inngest function to personalize all messages for a campaign.

    Args:
        ctx.event.data.campaign_id: ID of the Campaign
        ctx.event.data.force: Whether to force personalization even if already personalized

    Returns:
        dict: Results of the operation
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        force = ctx.event.data.get("force", False)

        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}

        logger.info(f"📝 Starting personalization for campaign ID: {campaign_id}")

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

        # Get all message assignments for this campaign
        query = MessageAssignment.objects.filter(campaign_id=campaign_id)
        if not force:
            query = query.filter(personlized_msg_to_send='')

        count = query.count()
        if count == 0:
            return {
                'status': 'success',
                'message': 'No messages to personalize',
                'campaign_id': campaign_id
            }

        # Send events for each message assignment
        for message_assignment in query:
            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/personalize.message",
                    data={
                        "message_assignment_id": message_assignment.id,
                        "skip": True
                    }
                )
            )

        return {
            'status': 'success',
            'message': f'Scheduled personalization for {count} messages',
            'campaign_id': campaign_id
        }

    except Exception as e:
        logger.error(f"Error personalizing campaign messages {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }















@inngest_client.create_function(
    fn_id="send_email",
    trigger=inngest.TriggerEvent(event="campaigns/send.email"),
)
def send_email_task(ctx: inngest.Context):
    """
    Inngest function to send an email for a message assignment.
    Respects daily email sending limits.

    Args:
        ctx.event.data.message_assignment_id: ID of the MessageAssignment to send
        ctx.event.data.campaign_id: ID of the Campaign

    Returns:
        dict: Result of the operation
    """
    try:
        message_assignment_id = ctx.event.data.get("message_assignment_id")
        campaign_id = ctx.event.data.get("campaign_id")

        if not message_assignment_id or not campaign_id:
            return {"status": "error", "message": "message_assignment_id and campaign_id are required"}

        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return {"status": "error", "message": "Campaign not found", "campaign_id": campaign_id}

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)

        # Check if it has personalized content and hasn't been sent
        if not message_assignment.personlized_msg_to_send:
            return {"status": "error", "message": "No personalized content", "message_assignment_id": message_assignment_id}

        if message_assignment.sent:
            return {"status": "success", "message": "already sent", "message_assignment_id": message_assignment_id}

        # Send the email using the existing function
        from campaign.email_sender import send_campaign_email
        success = send_campaign_email(message_assignment, campaign)

        if success:
            logger.info(f"✅ Email sent successfully to {message_assignment.campaign_lead.lead.email}")
            return {"status": "success", "message_assignment_id": message_assignment_id}
        else:
            logger.error(f"❌ Failed to send email to {message_assignment.campaign_lead.lead.email}")
            return {"status": "error", "message": "Failed to send email", "message_assignment_id": message_assignment_id}

    except MessageAssignment.DoesNotExist:
        return {"status": "error", "message": "MessageAssignment not found", "message_assignment_id": message_assignment_id}
    except Exception as e:
        logger.error(f"Error sending email {message_assignment_id}: {str(e)}")
        return {"status": "error", "message": str(e), "message_assignment_id": message_assignment_id}



















@inngest_client.create_function(
    fn_id="send_campaign_emails",
    trigger=inngest.TriggerEvent(event="campaigns/send.campaign_emails"),
)
def send_campaign_emails_task(ctx: inngest.Context):
    """
    Inngest function to send emails for all message assignments in a campaign.

    Args:
        ctx.event.data.campaign_id: ID of the Campaign
        ctx.event.data.only_personalized: Only send emails that have personalized content

    Returns:
        dict: Results of the operation
    """
    try:
        campaign_id = ctx.event.data.get("campaign_id")
        only_personalized = ctx.event.data.get("only_personalized", True)

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

        # Get all message assignments for this campaign that haven't been sent
        query = MessageAssignment.objects.filter(
            campaign_id=campaign_id,
            sent=False
        )

        if only_personalized:
            query = query.filter(personlized_msg_to_send__gt='')

        count = query.count()

        if count == 0:
            return {
                'status': 'success',
                'message': 'No emails to send',
                'campaign_id': campaign_id
            }

        # Send events for each message assignment
        for message_assignment in query:
            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/send.email",
                    data={
                        "message_assignment_id": message_assignment.id,
                        "campaign_id": campaign_id
                    }
                )
            )

        return {
            'status': 'success',
            'message': f'Scheduled sending for {count} emails',
            'campaign_id': campaign_id
        }

    except Exception as e:
        logger.error(f"Error sending campaign emails {campaign_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }











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
