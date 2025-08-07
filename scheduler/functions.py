from datetime import timedelta, datetime
from django.utils import timezone
import logging

import inngest

from .client import inngest_client

logger = logging.getLogger(__name__)


# Create an Inngest function
@inngest_client.create_function(
    fn_id="campaign_scheduler",
    # Event that triggers this function
    trigger=inngest.TriggerEvent(event="campaigns/campaign.scheduled"),
)
def campaign_scheduler(ctx: inngest.Context):
    """
    Schedules a campaign based on its schedule settings.
    This is the main entry point for campaign launching with timezone-aware scheduling.
    """
    campaign_id = ctx.event.data.get("object_id")
    logger.info(f"🎯 Campaign scheduler triggered for campaign ID: {campaign_id}")

    if not campaign_id:
        return {"status": "error", "message": "campaign_id (object_id) is required"}

    try:
        # Get the campaign and its schedule
        from campaign.models import Campaign
        from campaign.scheduling_utils import create_scheduler_from_campaign, get_immediate_send_time

        campaign = Campaign.objects.get(id=campaign_id)
        scheduler = create_scheduler_from_campaign(campaign)

        if scheduler:
            # Campaign has a schedule - use smart scheduling
            logger.info(f"📅 Using scheduled delivery for campaign {campaign_id}")

            # Get schedule summary for logging
            schedule_summary = scheduler.get_schedule_summary()
            logger.info(f"📋 Schedule: {schedule_summary}")

            # Calculate next valid send time
            next_send_time = scheduler.get_next_valid_send_time()

            # Validate timestamp for Inngest
            timestamp = int(next_send_time.timestamp())
            min_timestamp = int(datetime(1980, 1, 2).timestamp())

            if timestamp < min_timestamp:
                logger.error(f"❌ Calculated timestamp {timestamp} is before 1980 minimum {min_timestamp}")
                logger.error(f"❌ Next send time: {next_send_time}")
                logger.error(f"❌ Schedule start date: {scheduler.start_date}")
                return {
                    "status": "error",
                    "message": f"Invalid timestamp: {next_send_time} is before 1980",
                    "campaign_id": campaign_id
                }

            logger.info(f"⏰ Scheduling for timestamp: {timestamp} ({next_send_time})")

            # Schedule the email processing for the calculated time
            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/process_scheduled_emails",
                    data={
                        "campaign_id": campaign_id,
                        "scheduled_time": next_send_time.isoformat()
                    },
                    ts=timestamp  # Schedule for specific time
                )
            )

            logger.info(f"⏰ Campaign {campaign_id} scheduled for {next_send_time}")

            return {
                "status": "success",
                "message": f"Campaign scheduled for {next_send_time}",
                "campaign_id": campaign_id,
                "scheduled_time": next_send_time.isoformat(),
                "schedule_summary": schedule_summary
            }

        else:
            # No schedule found - send immediately
            logger.info(f"🚀 No schedule found, sending campaign {campaign_id} immediately")

            send_time = get_immediate_send_time()

            # Validate timestamp for Inngest
            timestamp = int(send_time.timestamp())
            min_timestamp = int(datetime(1980, 1, 2).timestamp())

            if timestamp < min_timestamp:
                logger.error(f"❌ Immediate timestamp {timestamp} is before 1980 minimum {min_timestamp}")
                return {
                    "status": "error",
                    "message": f"Invalid immediate timestamp: {send_time} is before 1980",
                    "campaign_id": campaign_id
                }

            logger.info(f"⏰ Immediate scheduling for timestamp: {timestamp} ({send_time})")

            inngest_client.send_sync(
                inngest.Event(
                    name="campaigns/process_scheduled_emails",
                    data={
                        "campaign_id": campaign_id,
                        "scheduled_time": send_time.isoformat()
                    },
                    ts=timestamp
                )
            )

            return {
                "status": "success",
                "message": "Campaign scheduled for immediate delivery",
                "campaign_id": campaign_id,
                "scheduled_time": send_time.isoformat()
            }

    except Campaign.DoesNotExist:
        error_msg = f"Campaign {campaign_id} not found"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

    except Exception as e:
        error_msg = f"Error scheduling campaign {campaign_id}: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}