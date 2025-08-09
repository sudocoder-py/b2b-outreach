from campaign.models import Campaign
from django.template.response import TemplateResponse

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    



def is_campaign_view_only(campaign_id):

    try:
        campaign = Campaign.objects.get(pk=campaign_id)
        if campaign.is_locked_for_editing():
            is_view_only = True
        else:     
            is_view_only = False

    except Campaign.DoesNotExist:
        pass

    return is_view_only