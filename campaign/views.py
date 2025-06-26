from django.shortcuts import redirect, get_object_or_404, render
from django.http import Http404
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
    
    return render(request, "app/campaign/dashboard.html")


def campaign_leads(request, pk):
    
    return render(request, "app/campaign/campaign-leads.html")


def campaign_sequence(request, pk):
    
    return render(request, "app/campaign/sequence.html")    




def campaign_scheduele(request, pk):
    
    return render(request, "app/campaign/scheduele.html")       




def campaign_options(request, pk):
    
    return render(request, "app/campaign/options.html")     