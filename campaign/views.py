from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Link
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
    
    return render(request, "app/leads/leads-view.html")


def campaign_view_list(request):
    
    return render(request, "app/campaign/view-list.html")


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
    context = {
        'campaign_id': pk,
        'current_tab': 'sequences'
    }
    return render(request, "app/campaign/sequence.html", context)




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



