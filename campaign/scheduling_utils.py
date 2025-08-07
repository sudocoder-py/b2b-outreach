"""
Email Campaign Scheduling Utilities

This module provides timezone-aware scheduling logic for email campaigns,
including optimal send time calculation and batch distribution.
"""

import pytz
from datetime import datetime, timedelta, time
from django.utils import timezone
from datetime import timezone as dt_timezone
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class CampaignScheduler:
    """
    Handles timezone-aware email campaign scheduling with intelligent batch distribution.
    """
    
    def __init__(self, schedule_config: Dict, force_start_date: Optional[datetime] = None):
        """
        Initialize scheduler with campaign schedule configuration.

        Args:
            schedule_config: Dict containing:
                - start_date: datetime (will be overridden if force_start_date provided)
                - timing_from: str (HH:MM format)
                - timing_to: str (HH:MM format)
                - time_zone: str (timezone name)
                - days: List[str] (day codes like ['mon', 'tue'])
            force_start_date: Optional datetime to override the schedule's start_date
        """
        # Use forced start date if provided, otherwise use schedule's start date
        self.start_date = force_start_date if force_start_date else schedule_config['start_date']
        self.timing_from = schedule_config['timing_from']
        self.timing_to = schedule_config['timing_to']
        self.timezone_name = schedule_config['time_zone']
        self.allowed_days = schedule_config['days']
        
        # Convert to timezone object
        self.timezone = pytz.timezone(self.timezone_name)
        
        # Convert time strings to time objects
        self.from_time = self._parse_time(self.timing_from)
        self.to_time = self._parse_time(self.timing_to)
        
        # Day mapping
        self.day_mapping = {
            'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
            'fri': 4, 'sat': 5, 'sun': 6
        }
    
    def _parse_time(self, time_str: str) -> time:
        """Parse time string (HH:MM) to time object."""
        hour, minute = map(int, time_str.split(':'))
        return time(hour, minute)
    
    def _is_allowed_day(self, dt: datetime) -> bool:
        """Check if the given datetime falls on an allowed day."""
        weekday = dt.weekday()
        day_codes = [code for code, num in self.day_mapping.items() if num == weekday]
        return any(day in self.allowed_days for day in day_codes)
    
    def _is_within_time_window(self, dt: datetime) -> bool:
        """Check if the given datetime is within the allowed time window."""
        dt_time = dt.time()
        return self.from_time <= dt_time <= self.to_time
    
    def get_next_valid_send_time(self, from_datetime: Optional[datetime] = None) -> datetime:
        """
        Get the next valid send time based on schedule constraints.

        Args:
            from_datetime: Starting point (defaults to schedule start date)

        Returns:
            Next valid datetime for sending emails
        """
        # Force to use current time if no from_datetime provided (safer approach)
        if from_datetime is None:
            from_datetime = timezone.now()

        # Ensure timestamp is after 1980 (Inngest requirement)
        min_timestamp = datetime(1980, 1, 2, tzinfo=dt_timezone.utc)

        # Force from_datetime to be at least the minimum timestamp
        if from_datetime < min_timestamp:
            logger.warning(f"from_datetime {from_datetime} is before 1980, using minimum timestamp")
            from_datetime = min_timestamp

        # Convert to campaign timezone
        current_dt = from_datetime.astimezone(self.timezone)

        # Ensure we don't go before current time (always use now or later)
        now_in_tz = timezone.now().astimezone(self.timezone)

        if current_dt < now_in_tz:
            current_dt = now_in_tz

        logger.info(f"🕐 Starting search from {current_dt} in timezone {self.timezone_name}")
        
        # Find next valid time
        max_attempts = 14  # Look up to 2 weeks ahead
        attempt = 0
        
        while attempt < max_attempts:
            # Check if current time is valid
            if self._is_allowed_day(current_dt) and self._is_within_time_window(current_dt):
                result_time = current_dt.astimezone(dt_timezone.utc)

                # Final safety check for 1980 minimum
                if result_time < min_timestamp:
                    logger.warning(f"Calculated time {result_time} is before 1980, using minimum timestamp")
                    return min_timestamp

                return result_time
            
            # If not in time window but on allowed day, move to start of window
            if self._is_allowed_day(current_dt) and current_dt.time() < self.from_time:
                current_dt = current_dt.replace(
                    hour=self.from_time.hour,
                    minute=self.from_time.minute,
                    second=0,
                    microsecond=0
                )
                result_time = current_dt.astimezone(dt_timezone.utc)

                # Final safety check for 1980 minimum
                if result_time < min_timestamp:
                    logger.warning(f"Calculated time {result_time} is before 1980, using minimum timestamp")
                    return min_timestamp

                return result_time
            
            # Move to next day at start time
            current_dt = (current_dt + timedelta(days=1)).replace(
                hour=self.from_time.hour,
                minute=self.from_time.minute,
                second=0,
                microsecond=0
            )
            attempt += 1
        
        # Fallback: return minimum timestamp if no valid time found
        logger.warning(f"No valid send time found within {max_attempts} days, using minimum timestamp")
        return min_timestamp
    
    def calculate_batch_send_times(self, total_emails: int, batch_size: int = 50) -> List[datetime]:
        """
        Calculate optimal send times for email batches.
        
        Args:
            total_emails: Total number of emails to send
            batch_size: Number of emails per batch
            
        Returns:
            List of datetime objects for batch sending
        """
        num_batches = (total_emails + batch_size - 1) // batch_size  # Ceiling division
        send_times = []
        
        current_time = self.get_next_valid_send_time()
        
        for batch_num in range(num_batches):
            send_times.append(current_time)
            
            # Calculate next send time (spread batches across time window)
            if batch_num < num_batches - 1:  # Not the last batch
                current_time = self._get_next_batch_time(current_time)
        
        return send_times
    
    def _get_next_batch_time(self, current_time: datetime, min_interval_minutes: int = 5) -> datetime:
        """
        Calculate the next batch send time with minimum interval.
        
        Args:
            current_time: Current batch send time
            min_interval_minutes: Minimum minutes between batches
            
        Returns:
            Next batch send time
        """
        next_time = current_time + timedelta(minutes=min_interval_minutes)
        
        # Convert to campaign timezone for validation
        next_time_tz = next_time.astimezone(self.timezone)
        
        # If still within time window and allowed day, use it
        if (self._is_allowed_day(next_time_tz) and 
            self._is_within_time_window(next_time_tz)):
            return next_time
        
        # Otherwise, find next valid time
        return self.get_next_valid_send_time(next_time)
    
    def get_schedule_summary(self) -> Dict:
        """Get a human-readable summary of the schedule."""
        day_names = {
            'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 
            'thu': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday', 'sun': 'Sunday'
        }
        
        allowed_day_names = [day_names[day] for day in self.allowed_days]
        
        return {
            'timezone': self.timezone_name,
            'time_window': f"{self.timing_from} - {self.timing_to}",
            'allowed_days': allowed_day_names,
            'start_date': self.start_date.isoformat(),
            'next_send_time': self.get_next_valid_send_time().isoformat()
        }


def create_scheduler_from_campaign(campaign) -> Optional[CampaignScheduler]:
    """
    Create a CampaignScheduler from a campaign object.

    Args:
        campaign: Campaign model instance

    Returns:
        CampaignScheduler instance or None if no schedule found
    """
    try:
        # Get the campaign's schedule
        schedule = campaign.schedule_set.first()

        if not schedule:
            logger.warning(f"No schedule found for campaign {campaign.id}")
            return None

        logger.info(f"📅 Found schedule for campaign {campaign.id}: start_date={schedule.start_date}")

        schedule_config = {
            'start_date': schedule.start_date,  # This will be overridden by force_start_date
            'timing_from': schedule.timing_from,
            'timing_to': schedule.timing_to,
            'time_zone': schedule.time_zone,
            'days': schedule.days
        }

        # Force the start date to be the schedule's start_date (ensuring we use the right date)
        return CampaignScheduler(schedule_config, force_start_date=schedule.start_date)

    except Exception as e:
        logger.error(f"Error creating scheduler for campaign {campaign.id}: {str(e)}")
        return None


def get_immediate_send_time() -> datetime:
    """Get immediate send time (for campaigns without scheduling)."""
    immediate_time = timezone.now() + timedelta(seconds=30)  # Small delay for processing

    # Ensure timestamp is after 1980 (Inngest requirement)
    min_timestamp = datetime(1980, 1, 2, tzinfo=dt_timezone.utc)
    if immediate_time < min_timestamp:
        logger.warning(f"Immediate time {immediate_time} is before 1980, using minimum timestamp")
        return min_timestamp

    return immediate_time


class EmailAccountRateLimiter:
    """
    Handles rate limiting and batch distribution across multiple email accounts.
    Respects individual account daily limits and minimum wait times.
    """

    def __init__(self, email_accounts: List):
        """
        Initialize with list of email account objects.

        Args:
            email_accounts: List of EmailAccount model instances
        """
        self.email_accounts = email_accounts
        self.account_info = []

        # Calculate total capacity and prepare account info
        total_daily_capacity = 0
        for account in email_accounts:
            remaining_capacity = max(0, account.daily_limit - account.emails_sent)
            total_daily_capacity += remaining_capacity

            self.account_info.append({
                'account': account,
                'daily_limit': account.daily_limit,
                'emails_sent': account.emails_sent,
                'remaining_capacity': remaining_capacity,
                'min_wait_time': account.min_wait_time,
                'last_send_time': None
            })

        self.total_daily_capacity = total_daily_capacity

        # Sort accounts by remaining capacity (highest first)
        self.account_info.sort(key=lambda x: x['remaining_capacity'], reverse=True)

    def can_send_emails(self, email_count: int) -> bool:
        """Check if we can send the requested number of emails today."""
        return self.total_daily_capacity >= email_count

    def get_capacity_summary(self) -> Dict:
        """Get a summary of email account capacities."""
        return {
            'total_accounts': len(self.email_accounts),
            'total_daily_capacity': self.total_daily_capacity,
            'account_details': [
                {
                    'email': info['account'].email,
                    'daily_limit': info['daily_limit'],
                    'emails_sent': info['emails_sent'],
                    'remaining_capacity': info['remaining_capacity'],
                    'min_wait_time': info['min_wait_time']
                }
                for info in self.account_info
            ]
        }

    def distribute_emails_across_accounts(self, total_emails: int) -> List[Dict]:
        """
        Distribute emails across accounts based on their capacity and limits.

        Args:
            total_emails: Total number of emails to distribute

        Returns:
            List of dicts with account assignments: [{'account': EmailAccount, 'email_count': int}]
        """
        if not self.can_send_emails(total_emails):
            raise ValueError(f"Cannot send {total_emails} emails. Daily capacity: {self.total_daily_capacity}")

        distribution = []
        remaining_emails = total_emails

        # Distribute emails proportionally based on remaining capacity
        for info in self.account_info:
            if remaining_emails <= 0:
                break

            if info['remaining_capacity'] > 0:
                # Calculate how many emails this account should handle
                emails_for_account = min(
                    info['remaining_capacity'],
                    remaining_emails
                )

                if emails_for_account > 0:
                    distribution.append({
                        'account': info['account'],
                        'email_count': emails_for_account,
                        'min_wait_time': info['min_wait_time']
                    })
                    remaining_emails -= emails_for_account

        return distribution

    def calculate_send_schedule(self, total_emails: int, start_time: datetime) -> List[Dict]:
        """
        Calculate when each email should be sent, respecting account wait times.

        Args:
            total_emails: Total number of emails to send
            start_time: When to start sending

        Returns:
            List of send schedules: [{'send_time': datetime, 'account': EmailAccount}]
        """
        distribution = self.distribute_emails_across_accounts(total_emails)
        send_schedule = []

        # Track next available time for each account
        account_next_time = {}
        for dist in distribution:
            account_next_time[dist['account'].id] = start_time

        # Create round-robin schedule to distribute load evenly
        email_assignments = []
        for dist in distribution:
            for _ in range(dist['email_count']):
                email_assignments.append({
                    'account': dist['account'],
                    'min_wait_time': dist['min_wait_time']
                })

        # Sort by account to ensure even distribution
        email_assignments.sort(key=lambda x: x['account'].id)

        # Calculate send times
        for assignment in email_assignments:
            account = assignment['account']
            min_wait = assignment['min_wait_time']

            send_time = account_next_time[account.id]
            send_schedule.append({
                'send_time': send_time,
                'account': account
            })

            # Update next available time for this account
            account_next_time[account.id] = send_time + timedelta(seconds=min_wait)

        # Sort by send time
        send_schedule.sort(key=lambda x: x['send_time'])

        return send_schedule


def create_rate_limiter_from_campaign(campaign) -> Optional[EmailAccountRateLimiter]:
    """
    Create an EmailAccountRateLimiter from a campaign's selected email accounts.

    Args:
        campaign: Campaign model instance

    Returns:
        EmailAccountRateLimiter instance or None if no email accounts found
    """
    try:
        # Get campaign options and selected email accounts
        campaign_options = campaign.campaign_options.first()

        if not campaign_options:
            logger.warning(f"No campaign options found for campaign {campaign.id}")
            return None

        email_accounts = list(campaign_options.email_accounts.filter(status='active'))

        if not email_accounts:
            logger.warning(f"No active email accounts found for campaign {campaign.id}")
            return None

        return EmailAccountRateLimiter(email_accounts)

    except Exception as e:
        logger.error(f"Error creating rate limiter for campaign {campaign.id}: {str(e)}")
        return None
