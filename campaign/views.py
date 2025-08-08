
from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q, Min
import pytz

from campaign.utils import get_or_none
from .dicts import timezone_options, days_options, time_options
from django.core.serializers.json import DjangoJSONEncoder
import json


from campaign.helpers import get_campaigns_and_products, get_company_email_accounts, get_company_products, get_lead_lists_or_both, get_messages_and_products, get_subscribed_company
from .models import Campaign, CampaignLead, CampaignOptions, CampaignStats, LeadList, Link, Message, MessageAssignment, Schedule
import logging

logger = logging.getLogger(__name__)

def redirect_and_track(request, ref_code):
    """
    Track the visit and redirect to the actual landing page

    This view:
    1. Looks up the Link by ref_code
    2. Records the visit
    3. Updates campaign stats if this is the first visit
    4. Redirects to the actual landing page with UTM parameters
    """
    try:
        # Find the link with this reference code
        link = get_object_or_404(Link, ref=ref_code)

        # Check if this is the first visit (before tracking)
        is_first_visit = link.visit_count == 0

        # Record the visit
        link.track_visit()

        # Update campaign stats if this is the first visit
        if is_first_visit and link.campaign:
            try:
                campaign_stats, _ = CampaignStats.objects.get_or_create(
                    campaign=link.campaign,
                    defaults={
                        'clicked_count': 0,
                        'sequence_started_count': 0,
                        'opened_count': 0,
                        'replied_count': 0,
                        'opportunities_count': 0,
                        'conversions_count': 0
                    }
                )
                # Increment clicked count
                campaign_stats.clicked_count += 1
                campaign_stats.save(update_fields=['clicked_count'])

                logger.info(f"Updated campaign stats: clicked_count incremented for campaign {link.campaign.id}")
            except Exception as stats_error:
                # Log the error but don't break the redirect
                logger.error(f"Error updating campaign stats: {str(stats_error)}")

        # Get the campaign lead for potential future use
        campaign_lead = link.campaign_lead
        if campaign_lead:
            # You could update additional stats here
            # For example, mark that this lead has engaged
            pass

        # Log the visit for debugging
        logger.info(f"Tracked visit for link {link.id} with ref {ref_code}")

        # Get the full URL with UTM parameters
        destination_url = link.full_url()

        # Redirect to the actual landing page
        return redirect(destination_url)

    except Exception as e:
        # Log the error but don't expose details to user
        logger.error(f"Error tracking link visit: {str(e)}")
        raise Http404("Link not found")






def leads_lists(request):
    lead_lists= get_lead_lists_or_both(request, lead_lists_only=True, list_id=None)

    context = {
        'lead_lists': lead_lists
    }

    return render(request, "app/leads/leads-lists.html", context)


def leads_view(request, pk):

    lead_lists, leads, = get_lead_lists_or_both(request, lead_lists_only=False, list_id=pk)
    lead_lists_assign= lead_lists.exclude(id=pk)

    context = {
        'leads': leads,
        'lead_list_id': pk,
        'lead_lists': lead_lists,
        'lead_lists_assign': lead_lists_assign
    }
    return render(request, "app/leads/leads-view.html", context)



def show_all_leads_view(request):

    lead_lists, leads, = get_lead_lists_or_both(request, lead_lists_only=False, list_id=None)

    context = {
        'leads': leads,
    }
    return render(request, "app/leads/all-leads-view.html", context)


def add_leads(request, pk):
    return render(request, "app/leads/add-leads.html", context={'lead_list_id': pk})



def create_campaign_view(request): 
    products= get_company_products(request)

    context = {
        'products': products,
    }

    return render(request, "app/campaign/add-new.html", context)








def campaign_view_list(request):
    campaigns, products= get_campaigns_and_products(request)
    campaigns_stats= CampaignStats.objects.filter(campaign__in=campaigns)

    context = {
        'campaigns': campaigns,
        'products': products,
        'campaigns_stats': campaigns_stats
    }

    return render(request, "app/campaign/view-list.html", context)


def campaign_dashboard(request, pk):
    campaign_status= Campaign.objects.get(id=pk, subscribed_company=get_subscribed_company(request)).status
    campaign_stats = get_or_none(CampaignStats, campaign=pk)
    context = {
        'campaign_id': pk,
        'current_tab': 'analytics',
        'status': campaign_status,
        'stats': campaign_stats
    }
    return render(request, "app/campaign/dashboard.html", context)


def campaign_leads(request, pk):
    
    all_lead_lists= get_lead_lists_or_both(request, lead_lists_only=True, list_id=None)
    lead_lists= all_lead_lists.filter(campaigns=pk)
    lead_lists_assign= all_lead_lists.exclude(campaigns__id=pk)

    context = {
        'campaign_id': pk,
        'current_tab': 'leads',
        'lead_lists': lead_lists,
        'lead_lists_assign': lead_lists_assign,
    }
    return render(request, "app/campaign/campaign-leads.html", context)



def campaign_sequence(request, pk):
    all_messages, products= get_messages_and_products(request)

    # Get unique messages with their assignment counts - use distinct() to avoid duplicates
    messages = all_messages.filter(
        messageassignment__campaign_id=pk
    ).annotate(
        total_assignments=Count('messageassignment'),
        sent_count=Count('messageassignment', filter=Q(messageassignment__sent=True)),
        response_count=Count('messageassignment', filter=Q(messageassignment__responded=True)),
        delayed_by_days=Min('messageassignment__delayed_by_days')
    ).distinct().order_by('id')  # Use distinct() and order by id for consistent ordering

    products= products.filter(product_campaigns=pk)
    all_messages= all_messages.filter(product__in=products)
    # here i wanna make all_messages.exclude the ones that are not in the campaign
    all_messages= all_messages.exclude(id__in=messages.values_list('id', flat=True))

    context = {
        'campaign_id': pk,
        'current_tab': 'sequences',
        'messages': messages,  # Now contains aggregated data without duplicates
        'all_messages': all_messages  # For the "Add" dropdown
    }
    return render(request, "app/campaign/sequence.html", context)




def campaign_scheduele(request, pk):
    timezones, days, times = timezone_options, days_options, time_options
    campaign = Campaign.objects.get(id=pk)
    campaign_Schedule = Schedule.objects.filter(campaign=campaign)
    
    context = {
        'campaign_id': pk,
        'current_tab': 'schedule',
        'timezones': timezones,
        'days': days,
        'times': times,
        'schedule': campaign_Schedule
    }
    return render(request, "app/campaign/scheduele.html", context)



def campaign_options(request, pk):
    # Get all email accounts for the company
    company_email_accounts = get_company_email_accounts(request)
    
    # Get all campaigns for the company (excluding current campaign if needed)
    campaigns, products = get_campaigns_and_products(request)
    
    # Get all email accounts used in any campaign options
    used_email_ids = set()
    for campaign in campaigns:
        # Skip current campaign if you don't want to mark emails used in current campaign as "used"
        if campaign.id == pk:
            continue
            
        campaign_options = CampaignOptions.objects.filter(campaign=campaign).first()
        if campaign_options:
            used_email_ids.update(campaign_options.email_accounts.values_list('id', flat=True))
    
    # Get selected emails for current campaign
    current_campaign_options = CampaignOptions.objects.filter(campaign_id=pk).first()
    
    # Prepare the email list in required format
    formatted_emails = []
    for email_account in company_email_accounts:
        formatted_emails.append({
            'email_id': email_account.id,
            'email': email_account.email,
            'active': email_account.status == 'active',
            'used': email_account.id in used_email_ids,
        })
    
    context = {
        'campaign_id': pk,
        'current_tab': 'options',
        'emails': formatted_emails,
        'campaign_options': current_campaign_options
    }
    return render(request, "app/campaign/options.html", context)



# New navigation views
def products_view(request):
    """Products management page"""

    products = get_company_products(request)
    
    context = {
        'products': products
    }
    return render(request, "app/products/products.html", context)




def email_accounts_view(request):
    """Email accounts management page"""
    
    email_accounts= get_company_email_accounts(request)

    context = {
        'emails': email_accounts
    }
    return render(request, "app/account/email-accounts.html", context)




def messages_view(request):
    """Messages management page"""
    messages, products = get_messages_and_products(request)

    message_stats = []

    for message in messages:
        # Get all assignments for this message
        assignments = MessageAssignment.objects.filter(message=message)
        total_assignments = assignments.count()

        # Opened
        opened_count = assignments.filter(opened=True).count()
        open_rate = (opened_count / total_assignments * 100) if total_assignments > 0 else 0

        # Replied
        replied_count = assignments.filter(responded=True).count()
        responded_rate = (replied_count / total_assignments * 100) if total_assignments > 0 else 0

        # Links and CTR
        links = Link.objects.filter(url_message_assignments__message=message).distinct()
        total_clicks = sum(link.visit_count for link in links)
        ctr = (total_clicks / total_assignments * 100) if total_assignments > 0 else 0

        # Opportunities
        opportunities = CampaignLead.objects.filter(
            messageassignment__message=message,
            opportunity_status__in=["positive", "won"]
        ).distinct().count()

        # Performance metric (opened + replied + clicked) / 3
        performance = (((opened_count + replied_count + total_clicks)/3) / total_assignments * 100) if total_assignments > 0 else 0 

        # Attach stats to the message object
        message.opened_count = opened_count
        message.open_rate = round(open_rate, 2)
        message.responded_count = replied_count
        message.responded_rate = round(responded_rate, 2)
        message.clicks = total_clicks
        message.ctr = round(ctr, 2)
        message.performance = round(performance, 2)
        message.opportunity_count = opportunities

        message_stats.append({
            "message": message,
            "opened": opened_count,
            "clicked": total_clicks,
            "replied": replied_count,
            "opportunities": opportunities
        })

    # Compute the "most" metrics
    most_opened = max(message_stats, key=lambda x: x["opened"], default=None)
    most_clicked = max(message_stats, key=lambda x: x["clicked"], default=None)
    most_replied = max(message_stats, key=lambda x: x["replied"], default=None)
    most_opportunity = max(message_stats, key=lambda x: x["opportunities"], default=None)

    context = {
        'messages': messages,
        'products': products,
        'most_opened': most_opened["message"] if most_opened else None,
        'most_clicked': most_clicked["message"] if most_clicked else None,
        'most_replied': most_replied["message"] if most_replied else None,
        'most_opportunity': most_opportunity["message"] if most_opportunity else None,
    }

    return render(request, "app/msgs/messages.html", context)



def messages_edit_view(request, pk):
    """Messages management page"""

    messages, products = get_messages_and_products(request)

    context = {
        'messages': messages,
        'message_id': pk,
        'products': products
    }
    return render(request, "app/msgs/messages-edit.html", context)


def messages_add_view(request):
    """Messages management page"""

    messages, products = get_messages_and_products(request)

    context = {
        'messages': messages,
        'products': products
    }

    return render(request, "app/msgs/messages-edit.html", context)


def links_view(request):
    """Links management page"""
    campaigns, products = get_campaigns_and_products(request)
    links = Link.objects.filter(campaign__in=campaigns)

    context = {
        'products': products,
        'campaigns': campaigns,
        'links': links
    }

    return render(request, "app/links.html", context)


def overall_dashboard_view(request):
    """Overall dashboard page"""
    return render(request, "app/overall-dashboard.html")


def feedback_view(request):
    """Feedback and feature requests page"""
    return render(request, "app/account/feedback.html")


def account_settings_view(request):
    """Account settings page"""
    return render(request, "app/account/account-settings.html")
