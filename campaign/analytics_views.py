from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Campaign, CampaignDailyStats
import json


@require_http_methods(["GET"])
def campaign_analytics_data(request, campaign_id):
    """
    API endpoint to get analytics data for a campaign dashboard.
    Supports time filtering: 24h, 7d, 4w, 3m, all
    """
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    # Get time filter from query params
    time_filter = request.GET.get('filter', '4w')  # Default to 4 weeks
    
    # Calculate date range based on filter
    end_date = timezone.now().date()
    
    if time_filter == '24h':
        start_date = end_date - timedelta(days=1)
    elif time_filter == '7d':
        start_date = end_date - timedelta(days=7)
    elif time_filter == '4w':
        start_date = end_date - timedelta(weeks=4)
    elif time_filter == '3m':
        start_date = end_date - timedelta(days=90)
    else:  # 'all' or any other value
        # Get the earliest date we have data for this campaign
        earliest_stats = CampaignDailyStats.objects.filter(
            campaign=campaign
        ).order_by('date').first()
        
        if earliest_stats:
            start_date = earliest_stats.date
        else:
            start_date = campaign.created_at.date()
    
    # Get daily stats for the date range
    daily_stats = CampaignDailyStats.objects.filter(
        campaign=campaign,
        date__range=(start_date, end_date)
    ).order_by('date')
    
    # Prepare data for Chart.js
    labels = []
    sent_data = []
    opens_data = []
    clicks_data = []
    replies_data = []
    opportunities_data = []
    
    # Fill in missing dates with zeros
    current_date = start_date
    stats_dict = {stat.date: stat for stat in daily_stats}
    
    while current_date <= end_date:
        # Format label based on time filter
        if time_filter == '24h':
            labels.append(current_date.strftime('%H:%M'))
        elif time_filter in ['7d', '4w']:
            labels.append(current_date.strftime('%m/%d'))
        else:
            labels.append(current_date.strftime('%b %d'))
        
        # Get stats for this date or use zeros
        if current_date in stats_dict:
            stat = stats_dict[current_date]
            sent_data.append(stat.emails_sent_today)
            opens_data.append(stat.opens_today)
            clicks_data.append(stat.clicks_today)
            replies_data.append(stat.replies_today)
            opportunities_data.append(stat.opportunities_today)
        else:
            sent_data.append(0)
            opens_data.append(0)
            clicks_data.append(0)
            replies_data.append(0)
            opportunities_data.append(0)
        
        current_date += timedelta(days=1)
    
    # Get current campaign stats for summary cards
    try:
        campaign_stats = campaign.campaignstats
        summary_stats = {
            'total_leads': campaign_stats.total_leads,
            'sequence_started_count': campaign_stats.sequence_started_count,
            'sequence_started_rate': campaign_stats.sequence_started_rate,
            'opened_count': campaign_stats.opened_count,
            'open_rate_percentage': campaign_stats.open_rate_percentage,
            'clicked_count': campaign_stats.clicked_count,
            'click_rate_percentage': campaign_stats.click_rate_percentage,
            'replied_count': campaign_stats.replied_count,
            'reply_rate_percentage': campaign_stats.reply_rate_percentage,
            'opportunities_count': campaign_stats.opportunities_count,
            'opportunities_total_value': float(campaign_stats.opportunities_total_value),
            'conversions_count': campaign_stats.conversions_count,
            'conversions_total_value': float(campaign_stats.conversions_total_value),
        }
    except:
        # Fallback if no stats exist yet
        summary_stats = {
            'total_leads': 0,
            'sequence_started_count': 0,
            'sequence_started_rate': 0,
            'opened_count': 0,
            'open_rate_percentage': 0,
            'clicked_count': 0,
            'click_rate_percentage': 0,
            'replied_count': 0,
            'reply_rate_percentage': 0,
            'opportunities_count': 0,
            'opportunities_total_value': 0,
            'conversions_count': 0,
            'conversions_total_value': 0,
        }
    
    return JsonResponse({
        'success': True,
        'time_filter': time_filter,
        'date_range': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'chart_data': {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Sent',
                    'data': sent_data,
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'borderColor': '#3b82f6',
                    'borderWidth': 3,
                    'fill': True
                },
                {
                    'label': 'Total opens',
                    'data': opens_data,
                    'backgroundColor': 'rgba(56, 189, 248, 0.1)',
                    'borderColor': '#38bdf8',
                    'borderWidth': 3,
                    'fill': True
                },
                {
                    'label': 'Total clicks',
                    'data': clicks_data,
                    'backgroundColor': 'rgba(245, 158, 11, 0.1)',
                    'borderColor': '#f59e0b',
                    'borderWidth': 3,
                    'fill': True
                },
                {
                    'label': 'Total replies',
                    'data': replies_data,
                    'backgroundColor': 'rgba(167, 139, 250, 0.1)',
                    'borderColor': '#a78bfa',
                    'borderWidth': 3,
                    'fill': True
                },
                {
                    'label': 'Opportunities',
                    'data': opportunities_data,
                    'backgroundColor': 'rgba(45, 212, 191, 0.1)',
                    'borderColor': '#2dd4bf',
                    'borderWidth': 3,
                    'fill': True
                }
            ]
        },
        'summary_stats': summary_stats
    })


@require_http_methods(["POST"])
def refresh_campaign_stats(request, campaign_id):
    """
    API endpoint to trigger a refresh of campaign stats.
    """
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    try:
        # Import here to avoid circular imports
        from .tasks import calculate_daily_stats_task
        
        # Schedule calculation for today
        task_result = calculate_daily_stats_task.delay(campaign_id)
        
        # Also update the main campaign stats
        from .models import CampaignStats
        stats, _ = CampaignStats.objects.get_or_create(campaign=campaign)
        stats.update_from_campaign()
        
        return JsonResponse({
            'success': True,
            'message': 'Stats refresh scheduled',
            'task_id': task_result.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error refreshing stats: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
def backfill_campaign_analytics(request, campaign_id):
    """
    API endpoint to backfill analytics data for a campaign.
    Useful for populating historical data.
    """
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    try:
        data = json.loads(request.body)
        start_date = data.get('start_date')  # YYYY-MM-DD format
        end_date = data.get('end_date')      # YYYY-MM-DD format
        
        if not start_date or not end_date:
            return JsonResponse({
                'success': False,
                'message': 'start_date and end_date are required'
            }, status=400)
        
        # Import here to avoid circular imports
        from .tasks import backfill_daily_stats_task
        
        # Schedule backfill task
        task_result = backfill_daily_stats_task.delay(campaign_id, start_date, end_date)
        
        return JsonResponse({
            'success': True,
            'message': f'Backfill scheduled from {start_date} to {end_date}',
            'task_id': task_result.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error scheduling backfill: {str(e)}'
        }, status=500)
