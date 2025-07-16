from django.db.models import Count
from clients.models import Product
from campaign.models import Lead, LeadList, Message, Campaign
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





def get_lead_lists_or_both(request, *, lead_lists_only=False, list_id=None):

    subscribed_company = get_subscribed_company(request)

    lead_lists = LeadList.objects.filter(subscribed_company=subscribed_company) \
                                 .annotate(count=Count('lead_lists'))

    if lead_lists_only:
        return lead_lists
    
    if list_id:
        leads = Lead.objects.filter(lead_list=list_id)
        return lead_lists, leads
    
    else:
        leads = Lead.objects.filter(subscribed_company=subscribed_company)
        return lead_lists, leads

