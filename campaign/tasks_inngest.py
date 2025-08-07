# testing inggest
import inngest
from scheduler.client import inngest_client

from celery import shared_task
from django.utils import timezone
from django.conf import settings
import logging
from datetime import timedelta
from .models import MessageAssignment
from .services import AnalyticsService



@shared_task(name="personalize_message_task")
def personalize_message_task(message_assignment_id, skip=True):
    """
    Celery task to personalize a message using AI and save it to the database.
    Rate limited to respect AI API limits.

    Args:
        message_assignment_id: ID of the MessageAssignment to personalize
        skip: If True, skip AI and use simple replacement

    Returns:
        bool: True if successful, False otherwise
    """
    try:

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)

        success = message_assignment.personalize_with_ai(skip=skip)

        if success:
            print(f"✅ Successfully personalized message for assignment ID {message_assignment_id}")

        return success

    except MessageAssignment.DoesNotExist:
        return False
    except Exception as e:
        return False

@shared_task(name="personalize_campaign_messages_task")
def personalize_campaign_messages_task(campaign_id, force=False):
    """
    Celery task to personalize all messages for a campaign.

    Args:
        campaign_id: ID of the Campaign
        force: Whether to force personalization even if already personalized

    Returns:
        dict: Results of the operation
    """
    try:
        print(f"📝 Starting personalization for campaign ID: {campaign_id}")

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

        # Create a task for each message assignment
        for message_assignment in query:
            personalize_message_task.delay(message_assignment.id)


        return {
            'status': 'success',
            'message': f'Scheduled personalization for {count} messages',
            'campaign_id': campaign_id
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }

@shared_task(name="send_email_task")
def send_email_task(message_assignment_id, campaign_id):
    """
    Celery task to send an email for a message assignment.
    Respects daily email sending limits.

    Args:
        message_assignment_id: ID of the MessageAssignment to send
        campaign_id: ID of the Campaign

    Returns:
        str/bool: "rate_limit_exceeded" if rate limit exceeded, True if successful, False otherwise
    """
    try:
        # Get the campaign object
        from .models import Campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return False

        # Get the message assignment
        message_assignment = MessageAssignment.objects.get(id=message_assignment_id)

        # Check if it has personalized content and hasn't been sent
        if not message_assignment.personlized_msg_to_send:
            return False

        if message_assignment.sent:
            return "already sent"

        # Send the email using the existing function
        from campaign.email_sender import send_campaign_email
        success = send_campaign_email(message_assignment, campaign)

        if success:
            print(f"✅ Email sent successfully to {message_assignment.campaign_lead.lead.email}")
        else:
            print(f"❌ Failed to send email to {message_assignment.campaign_lead.lead.email}")

        return success

    except MessageAssignment.DoesNotExist:
        return False
    except Exception as e:
        return False

@shared_task(name="send_campaign_emails_task")
def send_campaign_emails_task(campaign_id, only_personalized=True):
    """
    Celery task to send emails for all message assignments in a campaign.

    Args:
        campaign_id: ID of the Campaign
        only_personalized: Only send emails that have personalized content

    Returns:
        dict: Results of the operation
    """
    try:

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

        # Create a task for each message assignment
        for message_assignment in query:
            send_email_task.delay(message_assignment.id, campaign_id)


        return {
            'status': 'success',
            'message': f'Scheduled sending for {count} emails',
            'campaign_id': campaign_id
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }


def personalize_and_send_all_emails_at_once(campaign_id):
    """
    Celery task to personalize and send all emails at once for a specific campaign.

    Args:
        campaign_id: ID of the Campaign

    Returns:
        dict: Results of the operation
    """
    try:
       
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

        # First personalize all messages
       
        personalize_result = personalize_campaign_messages_task.delay(campaign_id=campaign_id, force=False)

        # Then send all personalized emails
        send_result = send_campaign_emails_task.delay(campaign_id=campaign_id, only_personalized=True)

        return {
            'status': 'success',
            'message': f'Campaign {campaign_id} launch initiated successfully',
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'personalize_task_id': personalize_result.id if hasattr(personalize_result, 'id') else None,
            'send_task_id': send_result.id if hasattr(send_result, 'id') else None
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'campaign_id': campaign_id
        }
