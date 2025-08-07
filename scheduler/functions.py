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
    print(ctx.event.data)
    return "done"
    