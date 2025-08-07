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
    """
    campaign_id = ctx.event.data.get("object_id")
    print(f"Campaign scheduler triggered for campaign ID: {campaign_id}")

    # Trigger the personalize and send all emails function
    inngest_client.send_sync(
        inngest.Event(
            name="campaigns/personalize_and_send.all_emails",
            data={"campaign_id": campaign_id}
        )
    )

    return {"status": "success", "campaign_id": campaign_id}