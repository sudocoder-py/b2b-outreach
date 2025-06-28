from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q


from campaign.helpers import get_company_products
from .models import Link, Message, MessageAssignment
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



def dashboard_non_functional(request):
    """
    Render the overall dashboard page
    """
    return render(request, 'overall-dashboard.html')



def dashboard(request):

    return render(request, "base-app.html")


def leads_view(request):
    # Simulate leads data with the exact structure you provided
    simulated_leads = [
        {
            'id': 1,
            'subscribed_company': 'fdudgames',
            'full_name': 'fdud ramo',
            'first_name': 'fdud',
            'last_name': 'ramo',
            'position': 'ceo',
            'email': 'fdudramo@gmail.com',
            'phone_number': None,
            'linkedin_profile': None,
            'company_name': 'fdudgames',
            'company_website': None,
            'industry': 'Gaming',
            'employee_count': 'N/A',
            'company_linkedin_page': None,
            'location': 'N/A',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 2,
            'subscribed_company': 'Elkood',
            'full_name': 'Yamen Alabsi',
            'first_name': 'Yamen',
            'last_name': 'Alabsi',
            'position': 'CEO & Co-founder‎‏ at Elkood',
            'email': 'yamenabsi@gmail.com',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/yamen-alabsi-669816164',
            'company_name': 'Elkood',
            'company_website': 'https://elkood.com/',
            'industry': 'IT Services',
            'employee_count': '11-50',
            'company_linkedin_page': None,
            'location': 'Riyadh, Saudi Arabia',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 3,
            'subscribed_company': 'Prootech Agency',
            'full_name': 'Salem AL-najjar',
            'first_name': 'Salem',
            'last_name': 'AL-najjar',
            'position': 'Ceo - founder at Prootech Agency',
            'email': 'mhmadnajjer2004@gmail.com',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/mohamad-salem-alnajjar-9a4069219',
            'company_name': 'Prootech Agency',
            'company_website': None,
            'industry': 'IT Services',
            'employee_count': '2-10',
            'company_linkedin_page': None,
            'location': 'Dubai, UAE',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 4,
            'subscribed_company': 'Pancode',
            'full_name': 'Ghassan Rizk',
            'first_name': 'Ghassan',
            'last_name': 'Rizk',
            'position': 'Chief Executive Officer at Pancode',
            'email': 'ghassanrizk@pan-code.com',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/ghassan-rizk-7a2266190',
            'company_name': 'Pancode',
            'company_website': 'http://www.pan-code.com',
            'industry': 'IT Services',
            'employee_count': '11-50',
            'company_linkedin_page': None,
            'location': 'Damascus, Syria',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 5,
            'subscribed_company': 'Florinz',
            'full_name': 'Gheias A.',
            'first_name': 'Gheias',
            'last_name': 'A.',
            'position': 'Co-founder - CEO at Florinz',
            'email': 'gy.alamin@hotmail.com',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/gheias-a-5392b498',
            'company_name': 'Florinz',
            'company_website': 'http://florinz.com',
            'industry': 'IT Services',
            'employee_count': '11-50',
            'company_linkedin_page': None,
            'location': 'Riyadh, Saudi Arabia',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 6,
            'subscribed_company': 'CodeGuru.ae',
            'full_name': 'Ashraf Altawashi',
            'first_name': 'Ashraf',
            'last_name': 'Altawashi',
            'position': 'Chief Executive Officer at CodeGuru.ae',
            'email': 'ashraf.altawashi@codeguru.ae',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/ashrafaltawashi',
            'company_name': 'CodeGuru.ae',
            'company_website': 'https://codeguru.ae',
            'industry': 'IT Services',
            'employee_count': '2-10',
            'company_linkedin_page': None,
            'location': 'Dubai, UAE',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 7,
            'subscribed_company': 'Zeolans Technologies',
            'full_name': 'Shameer Mohammed',
            'first_name': 'Shameer',
            'last_name': 'Mohammed',
            'position': 'Chief Executive Officer at Zeolans Technologies',
            'email': 'shameerkummalil@gmail.com',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin.com/in/shameer-mohammed-33051b59',
            'company_name': 'Zeolans Technologies',
            'company_website': 'https://www.zeolans.ae',
            'industry': 'IT Services',
            'employee_count': '11-50',
            'company_linkedin_page': None,
            'location': 'Dubai, UAE',
            'source': 'LinkedIn',
            'lead_type': 'Cold',
            'lead_type_class': 'badge-ghost',
            'lead_type_icon': 'fa-solid fa-snowflake',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 04, 2025',
        },
        {
            'id': 8,
            'subscribed_company': 'Raizer',
            'full_name': 'Razek Daoud',
            'first_name': 'Razek',
            'last_name': 'Daoud',
            'position': 'CEO',
            'email': 'razek.daoud@raizer.tech',
            'phone_number': None,
            'linkedin_profile': 'https://www.linkedin',
            'company_name': 'Raizer',
            'company_website': 'http://raizer.tech',
            'industry': 'Software Development',
            'employee_count': '11-50',
            'company_linkedin_page': None,
            'location': 'N/A',
            'source': 'LinkedIn',
            'lead_type': 'Warm',
            'lead_type_class': 'badge-warning',
            'lead_type_icon': 'fa-solid fa-fire',
            'source_class': 'badge-info',
            'source_icon': 'fa-brands fa-linkedin',
            'created_at': 'Jun 03, 2025',
        },
    ]

    # Calculate stats from the simulated data
    stats = {
        'total_leads': len(simulated_leads),
        'cold': len([l for l in simulated_leads if l['lead_type'] == 'Cold']),
        'warm': len([l for l in simulated_leads if l['lead_type'] == 'Warm']),
        'linkedin_source': len([l for l in simulated_leads if l['source'] == 'LinkedIn']),
        'it_industry': len([l for l in simulated_leads if 'IT' in l['industry']]),
    }

    context = {
        'leads': simulated_leads,
        'stats': stats,
    }
    return render(request, "app/leads/leads-view.html", context)



def campaign_view_list(request):
    simulated_campaigns =  [
        {
            'id': 1,
            'name': 'Q3 Tech Outreach',
            'product': 'SaaS Platform',
            'status': 'active',
            'leads': 500,
            'sent': 450,
            'clicked': 90,
            'replied': 25,
            'opportunities': 5
        },
        {
            'id': 2,
            'name': 'Summer Sale Promo',
            'product': 'E-commerce Goods',
            'status': 'completed',
            'leads': 2000,
            'sent': 1980,
            'clicked': 450,
            'replied': 120,
            'opportunities': 40
        },
        {
            'id': 3,
            'name': 'New Feature Launch',
            'product': 'Mobile App',
            'status': 'paused',
            'leads': 100,
            'sent': 50,
            'clicked': 10,
            'replied': 1,
            'opportunities': 0
        },
        {
            'id': 4,
            'name': 'MENA Expansion',
            'product': 'Enterprise Software',
            'status': 'draft',
            'leads': 0,
            'sent': 0,
            'clicked': 0,
            'replied': 0,
            'opportunities': 0
        }
    ]
    context = {
        'campaigns': simulated_campaigns,
    }

    return render(request, "app/campaign/view-list.html", context)


def campaign_dashboard(request, pk):
    context = {
        'campaign_id': pk,
        'current_tab': 'analytics'
    }
    return render(request, "app/campaign/dashboard.html", context)


def campaign_leads(request, pk):
    # Simulate campaign leads data
    simulated_leads = [
        {
            'id': 1,
            'email': 'john.doe@techcorp.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'company': 'TechCorp Inc.',
            'status': 'Not contacted',
            'status_class': 'badge-ghost',
            'status_icon': 'fa-regular fa-clock',
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
            'status_class': 'badge-info',
            'status_icon': 'fa-solid fa-paper-plane',
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
            'status_class': 'badge-success',
            'status_icon': 'fa-solid fa-reply',
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
            'status_class': 'badge-primary',
            'status_icon': 'fa-solid fa-circle-check',
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
            'status_class': 'badge-error',
            'status_icon': 'fa-solid fa-exclamation-triangle',
            'links_count': 0,
            'converted_at': None,
            'created_at': '2024-01-11',
        },
    ]

    # Calculate stats from the simulated data
    stats = {
        'total_leads': len(simulated_leads),
        'viewed': len([l for l in simulated_leads if l['status'] in ['Contacted', 'Replied', 'Converted']]),
        'contacted': len([l for l in simulated_leads if l['status'] in ['Contacted', 'Replied', 'Converted']]),
        'replied': len([l for l in simulated_leads if l['status'] in ['Replied', 'Converted']]),
        'interested': 0,  # None in our simulated data
        'converted': len([l for l in simulated_leads if l['status'] == 'Converted']),
    }

    context = {
        'campaign_id': pk,
        'current_tab': 'leads',
        'leads': simulated_leads,
        'stats': stats,
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
    context = {
        'campaign_id': pk,
        'current_tab': 'schedule'
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

    subscribed_company= request.user.subscribed_company
    products = get_company_products(subscribed_company)
    
    context = {
        'products': products
    }
    return render(request, "app/products.html", context)


def products_edit_view(request, pk):
    """Products management page"""
    return render(request, "app/products-edit.html")


def email_accounts_view(request):
    """Email accounts management page"""

    sampleAccounts = [
        {
            'id': 1,
            'email': "fdudromo@gmail.com",
            'connection_type': "IMAP/SMTP",
            'emails_sent': 1,
            'daily_limit': 30,
            'status': "connected"
        }
    ]
    context = {
        'emails': sampleAccounts
    }
    return render(request, "app/email-accounts.html", context)


def messages_view(request):
    """Messages management page"""
    subscribed_company= request.user.subscribed_company
    products = get_company_products(subscribed_company)
    messages = Message.objects.filter(product__in=products)

    context = {
        'messages': messages,
        'products': products
    }

    return render(request, "app/messages.html", context)


def messages_edit_view(request, pk):
    """Messages management page"""
    return render(request, "app/messages-edit.html")


def links_view(request):
    """Links management page"""
    return render(request, "app/links.html")


def overall_dashboard_view(request):
    """Overall dashboard page"""
    return render(request, "app/overall-dashboard.html")


def feedback_view(request):
    """Feedback and feature requests page"""
    return render(request, "app/feedback.html")


def account_settings_view(request):
    """Account settings page"""
    return render(request, "app/account-settings.html")
