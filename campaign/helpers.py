from django.db.models import Count
from django.shortcuts import get_object_or_404
from clients.models import Product
from campaign.models import Lead, LeadList, Message, Campaign, MessageAssignment
from django.core.exceptions import ImproperlyConfigured

def get_subscribed_company(request):
    subscribed_company = request.user.subscribed_company
    return subscribed_company


def get_company_products(request):
    subscribed_company= get_subscribed_company(request)
    products = Product.objects.filter(subscribed_company=subscribed_company)

    return products


def get_company_email_accounts(request):
    subscribed_company= get_subscribed_company(request)
    email_accounts = subscribed_company.email_accounts.all()

    return email_accounts





def get_messages_and_products(request):
    products = get_company_products(request)
    messages = Message.objects.filter(product__in=products)
    return messages, products

def get_campaigns_and_products(request):
    products = get_company_products(request)
    campaigns = Campaign.objects.filter(product__in=products)
    return campaigns, products


def get_campaign_status(request, campaign_id):
    campaign_status= Campaign.objects.get(id=campaign_id, subscribed_company=get_subscribed_company(request)).status
    return campaign_status


def get_lead_lists_or_both(request, *, lead_lists_only=False, list_id=None):

    subscribed_company = get_subscribed_company(request)

    lead_lists = LeadList.objects.filter(subscribed_company=subscribed_company) \
                                 .annotate(count=Count('lead_lists'))

    if lead_lists_only:
        return lead_lists
    
    if list_id:
        lead_list= get_object_or_404(LeadList, id=list_id)
        leads = Lead.objects.filter(lead_list=lead_list)
        return lead_lists, leads
    
    else:
        leads = Lead.objects.filter(subscribed_company=subscribed_company)
        return lead_lists, leads




def is_allowed_to_be_launched(request, pk):
    """
    check if the campaign is allowed to be launched
    """
    try:
        campaign = get_object_or_404(Campaign, pk=pk)

        campaign_leads = campaign.campaignlead_set.all()
        if campaign_leads.count() == 0:
            return {
                "allowed": False,
                "error": "campaign_leads_error",
                "message": "No campaign leads found for campaign",
                "campaign_id": pk
            }

    
        

        # Check if campaign has message assignments
        message_assignments_count = MessageAssignment.objects.filter(
            campaign=campaign,
            sent=False
        ).count()

        if message_assignments_count == 0:
            return {
                "allowed": False,
                "error": "message_assignments_error",
                "message": "No pending message assignments found for campaign",
                "campaign_id": pk
            }    

        campaign_options = campaign.campaign_options.first()
        if not campaign_options:
            return {
                "allowed": False,
                "error": "campaign_options_error",
                "message": "No options found for campaign",
                "campaign_id": pk
            }
        
        
        # # Check email accounts
        active_email_accounts = campaign_options.email_accounts.filter(status='active')
        if not active_email_accounts.exists():
            return {
                "allowed": False,
                "error": "email_accounts_error",
                "message": "No active email accounts found for campaign",
                "campaign_id": pk
            }
        

        return {
            "allowed": True,
            "message": "Campaign is allowed to be launched",
            "campaign_id": pk
        }


    except Exception as e:
        return {
            "allowed": False,
            "error": "unexpected_error",
            "message": f"Error checking campaign launch status: {str(e)}",
            "campaign_id": pk
        }


