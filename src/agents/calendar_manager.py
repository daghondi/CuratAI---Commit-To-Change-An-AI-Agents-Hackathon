"""
Calendar Manager Agent

Manages deadlines, schedules, and reminders for opportunities and submissions.
Integrates with user calendars (Google Calendar, Outlook).
Proactively alerts users to critical dates.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class ReminderType(Enum):
    """Types of reminders"""
    SUBMISSION_DEADLINE = "submission_deadline"
    FOLLOW_UP = "follow_up"
    RESPONSE_EXPECTED = "response_expected"
    PREPARATION = "preparation"


@dataclass
class CalendarEvent:
    """Represents a calendar event (deadline, reminder, etc.)"""
    event_id: str
    title: str
    date: str
    time: Optional[str] = None
    type: ReminderType = ReminderType.SUBMISSION_DEADLINE
    description: str = ""
    related_opportunity_id: Optional[str] = None
    related_submission_id: Optional[str] = None
    completed: bool = False
    reminders_sent: List[str] = field(default_factory=list)


class CalendarManager:
    """
    Calendar Agent: Manages deadlines, reminders, and scheduling.
    
    This agent:
    1. Extracts deadlines from opportunities and submissions
    2. Creates calendar events with reminders
    3. Sends proactive alerts (email, calendar invite, Slack)
    4. Tracks completion status
    5. Integrates with external calendar systems
    """
    
    def __init__(self, name: str = "Calendar Manager"):
        self.name = name
        self.calendar_events: List[CalendarEvent] = []
        self.reminder_schedule = {
            "1_week": timedelta(days=7),
            "3_days": timedelta(days=3),
            "1_day": timedelta(days=1),
        }
    
    def add_opportunity_to_calendar(
        self,
        opportunity_id: str,
        opportunity_title: str,
        deadline: str,
        organization: str
    ) -> CalendarEvent:
        """
        Add an opportunity deadline to the calendar.
        
        Args:
            opportunity_id: Unique ID of the opportunity
            opportunity_title: Title of the opportunity
            deadline: Deadline date (ISO format)
            organization: Organizing organization
            
        Returns:
            CalendarEvent object
        """
        logger.info(f"Calendar Manager: Adding {opportunity_title} to calendar (deadline: {deadline})")
        
        event = CalendarEvent(
            event_id=f"evt_{opportunity_id}_{datetime.now().timestamp()}",
            title=f"DEADLINE: {opportunity_title} ({organization})",
            date=deadline,
            type=ReminderType.SUBMISSION_DEADLINE,
            description=f"Submit proposal for {opportunity_title} at {organization}",
            related_opportunity_id=opportunity_id
        )
        
        self.calendar_events.append(event)
        
        # Schedule reminders
        self._schedule_reminders_for_event(event)
        
        return event
    
    def add_follow_up_to_calendar(
        self,
        submission_id: str,
        organization: str,
        follow_up_date: str
    ) -> CalendarEvent:
        """
        Add a follow-up reminder to the calendar.
        
        Args:
            submission_id: Related submission ID
            organization: Organization to follow up with
            follow_up_date: When to follow up (ISO format)
            
        Returns:
            CalendarEvent object
        """
        logger.info(f"Calendar Manager: Adding follow-up reminder for {submission_id}")
        
        event = CalendarEvent(
            event_id=f"evt_followup_{submission_id}_{datetime.now().timestamp()}",
            title=f"FOLLOW UP: {organization}",
            date=follow_up_date,
            type=ReminderType.FOLLOW_UP,
            description=f"Follow up on submission status with {organization}",
            related_submission_id=submission_id
        )
        
        self.calendar_events.append(event)
        
        # Single reminder on the day
        self._schedule_reminders_for_event(event)
        
        return event
    
    def _schedule_reminders_for_event(self, event: CalendarEvent):
        """
        Schedule reminders for an event based on type.
        
        Args:
            event: CalendarEvent to schedule reminders for
        """
        event_date = datetime.fromisoformat(event.date)
        now = datetime.now()
        
        # For submission deadlines, send reminders at 1 week, 3 days, 1 day
        if event.type == ReminderType.SUBMISSION_DEADLINE:
            for label, delta in self.reminder_schedule.items():
                reminder_date = event_date - delta
                if reminder_date > now:
                    event.reminders_sent.append(f"Scheduled: {label} before deadline")
                    logger.info(f"  → Reminder scheduled {label} before deadline")
        
        # For follow-ups, single reminder on the day
        elif event.type == ReminderType.FOLLOW_UP:
            event.reminders_sent.append("Scheduled: On day of follow-up")
            logger.info(f"  → Reminder scheduled for follow-up day")
    
    def get_upcoming_deadlines(self, days_ahead: int = 30) -> List[CalendarEvent]:
        """
        Get all upcoming deadlines within specified days.
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of upcoming CalendarEvent objects
        """
        now = datetime.now()
        future_date = now + timedelta(days=days_ahead)
        
        upcoming = []
        for event in self.calendar_events:
            if not event.completed:
                event_date = datetime.fromisoformat(event.date)
                if now <= event_date <= future_date:
                    upcoming.append(event)
        
        # Sort by date
        upcoming.sort(key=lambda x: x.date)
        
        logger.info(f"Calendar Manager: Found {len(upcoming)} upcoming deadlines")
        return upcoming
    
    def get_events_by_date(self, date: str) -> List[CalendarEvent]:
        """Get all events on a specific date"""
        return [e for e in self.calendar_events if e.date == date and not e.completed]
    
    def mark_event_complete(self, event_id: str):
        """Mark an event as completed"""
        for event in self.calendar_events:
            if event.event_id == event_id:
                event.completed = True
                logger.info(f"Calendar Manager: Marked {event.title} as complete")
                break
    
    def get_calendar_summary(self) -> Dict:
        """Get summary of calendar status"""
        upcoming = self.get_upcoming_deadlines(days_ahead=30)
        
        summary = {
            "total_events": len(self.calendar_events),
            "completed_events": sum(1 for e in self.calendar_events if e.completed),
            "upcoming_30_days": len(upcoming),
            "upcoming_events": [
                {
                    "title": e.title,
                    "date": e.date,
                    "days_until": (datetime.fromisoformat(e.date) - datetime.now()).days,
                    "type": e.type.value
                }
                for e in upcoming[:5]  # Top 5
            ],
            "critical_alerts": self._get_critical_alerts()
        }
        
        return summary
    
    def _get_critical_alerts(self) -> List[str]:
        """Identify critical upcoming deadlines (within 3 days)"""
        alerts = []
        now = datetime.now()
        critical_date = now + timedelta(days=3)
        
        for event in self.calendar_events:
            if not event.completed:
                event_date = datetime.fromisoformat(event.date)
                if now <= event_date <= critical_date:
                    days_left = (event_date - now).days
                    alerts.append(f"⚠️  {event.title} due in {days_left} days")
        
        return alerts
    
    def send_reminder(
        self,
        event_id: str,
        recipient_email: str,
        reminder_type: str = "email"
    ) -> bool:
        """
        Send reminder notification to user.
        
        In production, this would integrate with email, SMS, Slack, etc.
        
        Args:
            event_id: Event to remind about
            recipient_email: User's email
            reminder_type: Type of reminder (email, sms, slack, calendar_invite)
            
        Returns:
            Success status
        """
        event = None
        for e in self.calendar_events:
            if e.event_id == event_id:
                event = e
                break
        
        if not event:
            logger.warning(f"Calendar Manager: Event {event_id} not found")
            return False
        
        logger.info(f"Calendar Manager: Sending {reminder_type} reminder for {event.title} to {recipient_email}")
        
        # In production, this would actually send the reminder
        # For MVP, we just log it
        reminder_sent = f"Sent via {reminder_type}"
        event.reminders_sent.append(reminder_sent)
        
        return True


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    calendar = CalendarManager()
    
    # Add some opportunities to calendar
    print("\n=== Adding Events to Calendar ===\n")
    
    calendar.add_opportunity_to_calendar(
        opportunity_id="opp_001",
        opportunity_title="TED-style Talk on AI in Arts",
        deadline="2026-03-15",
        organization="CreativeAI Summit 2026"
    )
    
    calendar.add_opportunity_to_calendar(
        opportunity_id="opp_002",
        opportunity_title="Digital Arts Exhibition",
        deadline="2026-04-01",
        organization="ArtNow Gallery"
    )
    
    calendar.add_opportunity_to_calendar(
        opportunity_id="opp_003",
        opportunity_title="Creative Innovation Grant",
        deadline="2026-05-30",
        organization="National Endowment for the Arts"
    )
    
    # Add a follow-up reminder
    calendar.add_follow_up_to_calendar(
        submission_id="sub_001",
        organization="CreativeAI Summit",
        follow_up_date="2026-03-22"
    )
    
    # Get calendar summary
    print("\n=== Calendar Summary ===")
    summary = calendar.get_calendar_summary()
    
    print(f"Total Events: {summary['total_events']}")
    print(f"Upcoming (30 days): {summary['upcoming_30_days']}")
    print(f"\nCritical Alerts:")
    for alert in summary['critical_alerts']:
        print(f"  {alert}")
    
    print(f"\nUpcoming Events:")
    for event in summary['upcoming_events']:
        print(f"  • {event['title']} ({event['days_until']} days)")
    
    # Get upcoming deadlines
    print("\n=== Upcoming Deadlines (Next 30 Days) ===")
    upcoming = calendar.get_upcoming_deadlines(days_ahead=30)
    for event in upcoming:
        days_left = (datetime.fromisoformat(event.date) - datetime.now()).days
        print(f"  • {event.title} - {event.date} ({days_left} days left)")
