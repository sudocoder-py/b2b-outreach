from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
import pytz


from campaign.helpers import get_campaigns_and_products, get_company_email_accounts, get_company_products, get_lead_lists_or_both, get_messages_and_products, get_subscribed_company
from .models import Campaign, LeadList, Link, Message, MessageAssignment
import logging

logger = logging.getLogger(__name__)

def redirect_and_track(request, ref_code):
    """
    Track the visit and redirect to the actual landing page
    
    This view:
    1. Looks up the Link by ref_code
    2. Records the visit
    3. Redirects to the actual landing page with UTM parameters
    """
    try:
        # Find the link with this reference code
        link = get_object_or_404(Link, ref=ref_code)
        
        # Record the visit
        link.track_visit()
        
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

    context = {
        'leads': leads,
        'lead_list_id': pk,
        'lead_lists': lead_lists
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

    context = {
        'campaigns': campaigns,
        'products': products,
    }

    return render(request, "app/campaign/view-list.html", context)


def campaign_dashboard(request, pk):
    context = {
        'campaign_id': pk,
        'current_tab': 'analytics'
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


def campaign_leads_filter(request, pk):
    """HTMX endpoint for filtering leads"""
    # Get the same simulated data
    simulated_leads = [
        {
            'id': 1,
            'email': 'john.doe@techcorp.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'company': 'TechCorp Inc.',
            'status': 'Not contacted',
            'links_count': 3,
            'converted_at': None,
            'created_at': '2024-01-15',
        },
        {
            'id': 2,
            'email': 'sarah.wilson@innovate.io',
            'first_name': 'Sarah',
            'last_name': 'Wilson',
            'company': 'Innovate Solutions',
            'status': 'Contacted',
            'links_count': 2,
            'converted_at': None,
            'created_at': '2024-01-14',
        },
        {
            'id': 3,
            'email': 'mike.chen@startup.co',
            'first_name': 'Mike',
            'last_name': 'Chen',
            'company': 'Startup Co.',
            'status': 'Replied',
            'links_count': 1,
            'converted_at': None,
            'created_at': '2024-01-13',
        },
        {
            'id': 4,
            'email': 'lisa.brown@enterprise.com',
            'first_name': 'Lisa',
            'last_name': 'Brown',
            'company': 'Enterprise Corp',
            'status': 'Converted',
            'links_count': 4,
            'converted_at': '2024-01-20',
            'created_at': '2024-01-12',
        },
        {
            'id': 5,
            'email': 'alex.garcia@digital.net',
            'first_name': 'Alex',
            'last_name': 'Garcia',
            'company': 'Digital Networks',
            'status': 'Bounced',
            'links_count': 0,
            'converted_at': None,
            'created_at': '2024-01-11',
        },
    ]

    # Get filter parameters
    search_query = request.GET.get('search', '').lower().strip()
    status_filter = request.GET.get('status', '')

    # Filter leads
    filtered_leads = []
    for lead in simulated_leads:
        # Search filter
        search_text = f"{lead['first_name']} {lead['last_name']} {lead['email']} {lead['company']}".lower()
        matches_search = not search_query or search_query in search_text

        # Status filter
        matches_status = not status_filter or lead['status'] == status_filter

        if matches_search and matches_status:
            filtered_leads.append(lead)

    # Calculate stats for filtered leads
    stats = {
        'total_leads': len(filtered_leads),
        'viewed': len([l for l in filtered_leads if l['status'] in ['Contacted', 'Replied', 'Converted']]),
        'contacted': len([l for l in filtered_leads if l['status'] in ['Contacted', 'Replied', 'Converted']]),
        'replied': len([l for l in filtered_leads if l['status'] in ['Replied', 'Converted']]),
        'interested': 0,
        'converted': len([l for l in filtered_leads if l['status'] == 'Converted']),
    }

    context = {
        'campaign_id': pk,
        'leads': filtered_leads,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, "app/campaign/partials/leads-table.html", context)


def campaign_sequence(request, pk):
    # Get unique messages with their assignment counts
    messages = Message.objects.filter(
        messageassignment__campaign_id=pk
    ).annotate(
        total_assignments=Count('messageassignment'),
        sent_count=Count('messageassignment', filter=Q(messageassignment__sent=True)),
        response_count=Count('messageassignment', filter=Q(messageassignment__responded=True))
    ).order_by('-messageassignment__sent_at')

    context = {
        'campaign_id': pk,
        'current_tab': 'sequences',
        'messages': messages,  # Now contains aggregated data
        'all_messages': Message.objects.all()  # For the "Add" dropdown
    }
    return render(request, "app/campaign/sequence.html", context)



def campaign_sequence_message_assignments(request, message_id):
    assignments = MessageAssignment.objects.filter(
        message_id=message_id
    ).values(
        'id',
        'sent',
        'sent_at',
        'responded',
        'campaign_lead__lead__first_name',
        'campaign_lead__lead__last_name',
        'campaign_lead__lead__email'
    )
    return JsonResponse(list(assignments), safe=False)



def campaign_scheduele(request, pk):
    timezones = list(pytz.common_timezones)
    
    context = {
        'campaign_id': pk,
        'current_tab': 'schedule',
        'timezones': timezones,
    }
    return render(request, "app/campaign/scheduele.html", context)




def campaign_options(request, pk):
    context = {
        'campaign_id': pk,
        'current_tab': 'options'
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

    context = {
        'messages': messages,
        'products': products
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
