from datetime import timedelta, datetime
from django.utils import timezone

import inngest

from .client import inngest_client


# Create an Inngest function
@inngest_client.create_function(
    fn_id="campaign_scheduler",
    # Event that triggers this function
    trigger=inngest.TriggerEvent(event="campaigns/campaign.scheduled"),
)
def campaign_scheduler(ctx: inngest.Context):
    """
    Schedules a campaign for a future date.
    This is the main entry point for campaign launching.
    """
    campaign_id = ctx.event.data.get("object_id")
    print(f"🎯 Campaign scheduler triggered for campaign ID: {campaign_id}")

    if not campaign_id:
        return {"status": "error", "message": "campaign_id (object_id) is required"}

    # Trigger the personalize and send all emails function
    # This will handle everything in one efficient function call
    inngest_client.send_sync(
        inngest.Event(
            name="campaigns/personalize_and_send.all_emails",
            data={"campaign_id": campaign_id}
        )
    )

    return {"status": "success", "message": "Campaign launch initiated", "campaign_id": campaign_id}