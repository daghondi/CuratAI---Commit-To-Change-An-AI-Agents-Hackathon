"""
Multi-User Platform Foundation for CuratAI
Supports multiple artists with their own dashboards and data
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class UserAccount:
    """User account with profile and settings"""
    user_id: str
    email: str
    artist_name: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    preferences: Dict = field(default_factory=dict)
    subscription_tier: str = "free"  # free, pro, enterprise


@dataclass
class UserDashboard:
    """User's personal dashboard with metrics and data"""
    user_id: str
    dashboard_id: str
    created_at: datetime
    opportunities_tracked: int = 0
    proposals_created: int = 0
    submissions_made: int = 0
    acceptance_rate: float = 0.0
    followers: List[str] = field(default_factory=list)
    saved_opportunities: List[str] = field(default_factory=list)


@dataclass
class UserNotification:
    """Notification for user"""
    notification_id: str
    user_id: str
    message: str
    notification_type: str  # deadline, submission_accepted, opportunity, system
    created_at: datetime
    read: bool = False
    action_url: Optional[str] = None


class MultiUserPlatform:
    """
    Multi-user platform supporting multiple artists
    Each user has isolated data but shared resources
    """
    
    def __init__(self):
        self.users: Dict[str, UserAccount] = {}
        self.dashboards: Dict[str, UserDashboard] = {}
        self.notifications: Dict[str, List[UserNotification]] = {}
        self.user_data: Dict[str, Dict] = {}  # Opportunity tracking per user
    
    def create_user(self, email: str, artist_name: str, 
                   preferences: Dict = None) -> UserAccount:
        """
        Create new user account
        
        Args:
            email: User email
            artist_name: Artist's display name
            preferences: User preferences (notifications, privacy, etc)
        """
        user_id = str(uuid.uuid4())
        user = UserAccount(
            user_id=user_id,
            email=email,
            artist_name=artist_name,
            created_at=datetime.now(),
            preferences=preferences or {
                'notifications': True,
                'email_digest': 'daily',
                'privacy': 'private',
                'show_in_directory': False
            }
        )
        
        self.users[user_id] = user
        self.notifications[user_id] = []
        
        # Create dashboard
        dashboard = UserDashboard(
            user_id=user_id,
            dashboard_id=str(uuid.uuid4()),
            created_at=datetime.now()
        )
        self.dashboards[dashboard.dashboard_id] = dashboard
        
        # Initialize user data storage
        self.user_data[user_id] = {
            'opportunities': {},
            'proposals': {},
            'submissions': {},
            'strategy_data': {}
        }
        
        return user
    
    def get_user_dashboard(self, user_id: str) -> Optional[Dict]:
        """Get user's dashboard with metrics"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        dashboard = next(
            (d for d in self.dashboards.values() if d.user_id == user_id),
            None
        )
        
        if not dashboard:
            return None
        
        user_stats = self.user_data.get(user_id, {})
        
        return {
            'user_id': user_id,
            'artist_name': user.artist_name,
            'email': user.email,
            'joined': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'metrics': {
                'opportunities_tracked': len(user_stats.get('opportunities', {})),
                'proposals_created': len(user_stats.get('proposals', {})),
                'submissions_made': len(user_stats.get('submissions', {})),
                'acceptance_rate': dashboard.acceptance_rate
            },
            'subscription': user.subscription_tier,
            'preferences': user.preferences
        }
    
    def track_opportunity(self, user_id: str, opportunity_id: str,
                         opportunity_data: Dict) -> Dict:
        """
        User tracks an opportunity
        Stored in user's private data
        """
        if user_id not in self.user_data:
            return {'error': 'User not found'}
        
        self.user_data[user_id]['opportunities'][opportunity_id] = {
            'data': opportunity_data,
            'tracked_at': datetime.now().isoformat(),
            'status': 'tracked'
        }
        
        return {
            'success': True,
            'opportunity_id': opportunity_id,
            'message': 'Opportunity saved to your dashboard'
        }
    
    def save_proposal(self, user_id: str, opportunity_id: str,
                     proposal_data: Dict) -> Dict:
        """Save proposal draft for user"""
        if user_id not in self.user_data:
            return {'error': 'User not found'}
        
        proposal_id = str(uuid.uuid4())
        self.user_data[user_id]['proposals'][proposal_id] = {
            'opportunity_id': opportunity_id,
            'data': proposal_data,
            'created_at': datetime.now().isoformat(),
            'status': 'draft'
        }
        
        return {
            'success': True,
            'proposal_id': proposal_id,
            'message': 'Proposal saved to drafts'
        }
    
    def submit_proposal(self, user_id: str, proposal_id: str,
                       organization: str) -> Dict:
        """
        Submit proposal to opportunity
        Creates submission record and sends notifications
        """
        if user_id not in self.user_data:
            return {'error': 'User not found'}
        
        proposal = self.user_data[user_id]['proposals'].get(proposal_id)
        if not proposal:
            return {'error': 'Proposal not found'}
        
        submission_id = str(uuid.uuid4())
        submission = {
            'proposal_id': proposal_id,
            'organization': organization,
            'submitted_at': datetime.now().isoformat(),
            'status': 'submitted'
        }
        
        self.user_data[user_id]['submissions'][submission_id] = submission
        proposal['status'] = 'submitted'
        
        # Send notification
        self._send_notification(
            user_id,
            f"Proposal submitted to {organization}",
            'submission',
            f"/submissions/{submission_id}"
        )
        
        return {
            'success': True,
            'submission_id': submission_id,
            'message': f'Proposal submitted to {organization}'
        }
    
    def send_notification(self, user_id: str, message: str,
                        notification_type: str,
                        action_url: str = None) -> UserNotification:
        """Send notification to user"""
        return self._send_notification(user_id, message, notification_type, action_url)
    
    def _send_notification(self, user_id: str, message: str,
                          notification_type: str,
                          action_url: str = None) -> UserNotification:
        """Internal notification sending"""
        notification = UserNotification(
            notification_id=str(uuid.uuid4()),
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            created_at=datetime.now(),
            action_url=action_url
        )
        
        if user_id in self.notifications:
            self.notifications[user_id].append(notification)
        
        return notification
    
    def get_unread_notifications(self, user_id: str) -> List[Dict]:
        """Get unread notifications for user"""
        if user_id not in self.notifications:
            return []
        
        unread = [
            {
                'id': notif.notification_id,
                'message': notif.message,
                'type': notif.notification_type,
                'created_at': notif.created_at.isoformat(),
                'action_url': notif.action_url
            }
            for notif in self.notifications[user_id]
            if not notif.read
        ]
        
        return unread
    
    def mark_notification_read(self, user_id: str,
                              notification_id: str) -> bool:
        """Mark notification as read"""
        if user_id not in self.notifications:
            return False
        
        for notif in self.notifications[user_id]:
            if notif.notification_id == notification_id:
                notif.read = True
                return True
        
        return False
    
    def get_user_opportunities(self, user_id: str) -> List[Dict]:
        """Get user's tracked opportunities"""
        if user_id not in self.user_data:
            return []
        
        opportunities = self.user_data[user_id]['opportunities']
        return [
            {
                'opportunity_id': opp_id,
                **opp_data
            }
            for opp_id, opp_data in opportunities.items()
        ]
    
    def get_user_proposals(self, user_id: str) -> List[Dict]:
        """Get user's proposals"""
        if user_id not in self.user_data:
            return []
        
        proposals = self.user_data[user_id]['proposals']
        return [
            {
                'proposal_id': prop_id,
                **prop_data
            }
            for prop_id, prop_data in proposals.items()
        ]
    
    def update_user_preference(self, user_id: str, preference_key: str,
                              value: any) -> bool:
        """Update user preference"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        user.preferences[preference_key] = value
        return True
    
    def upgrade_subscription(self, user_id: str, tier: str) -> Dict:
        """Upgrade user subscription tier"""
        user = self.users.get(user_id)
        if not user:
            return {'error': 'User not found'}
        
        # Validate tier
        valid_tiers = ['free', 'pro', 'enterprise']
        if tier not in valid_tiers:
            return {'error': f'Invalid tier. Must be one of {valid_tiers}'}
        
        old_tier = user.subscription_tier
        user.subscription_tier = tier
        
        return {
            'success': True,
            'old_tier': old_tier,
            'new_tier': tier,
            'message': f'Upgraded from {old_tier} to {tier}'
        }


class PlatformAnalytics:
    """Platform-wide analytics and insights"""
    
    def __init__(self, platform: MultiUserPlatform):
        self.platform = platform
    
    def get_platform_stats(self) -> Dict:
        """Get overall platform statistics"""
        total_users = len(self.platform.users)
        active_users = sum(
            1 for user in self.platform.users.values()
            if user.is_active
        )
        
        total_opportunities = sum(
            len(data.get('opportunities', {}))
            for data in self.platform.user_data.values()
        )
        
        total_proposals = sum(
            len(data.get('proposals', {}))
            for data in self.platform.user_data.values()
        )
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_opportunities_tracked': total_opportunities,
            'total_proposals_created': total_proposals,
            'users_by_tier': self._get_tier_distribution()
        }
    
    def _get_tier_distribution(self) -> Dict:
        """Get distribution of users by subscription tier"""
        distribution = {'free': 0, 'pro': 0, 'enterprise': 0}
        for user in self.platform.users.values():
            distribution[user.subscription_tier] += 1
        return distribution
    
    def get_user_leaderboard(self, metric: str = 'submissions',
                             limit: int = 10) -> List[Dict]:
        """Get leaderboard of top users by metric"""
        user_metrics = []
        
        for user_id, user_data in self.platform.user_data.items():
            user = self.platform.users.get(user_id)
            if not user:
                continue
            
            if metric == 'submissions':
                count = len(user_data.get('submissions', {}))
            elif metric == 'proposals':
                count = len(user_data.get('proposals', {}))
            elif metric == 'opportunities':
                count = len(user_data.get('opportunities', {}))
            else:
                continue
            
            user_metrics.append({
                'user_id': user_id,
                'artist_name': user.artist_name,
                'count': count
            })
        
        # Sort and limit
        user_metrics.sort(key=lambda x: x['count'], reverse=True)
        return user_metrics[:limit]


# Demo usage
if __name__ == "__main__":
    print("👥 Multi-User Platform Foundation")
    print("=" * 60)
    
    platform = MultiUserPlatform()
    
    # Create users
    print("\n📝 Creating User Accounts...")
    user1 = platform.create_user(
        email="alexandra@example.com",
        artist_name="Alexandra Chen"
    )
    print(f"✅ User created: {user1.artist_name} (ID: {user1.user_id[:8]}...)")
    
    user2 = platform.create_user(
        email="james@example.com",
        artist_name="James Smith"
    )
    print(f"✅ User created: {user2.artist_name} (ID: {user2.user_id[:8]}...)")
    
    # Get dashboard
    print("\n📊 User Dashboard:")
    dashboard = platform.get_user_dashboard(user1.user_id)
    print(f"   Artist: {dashboard['artist_name']}")
    print(f"   Joined: {dashboard['joined']}")
    print(f"   Subscription: {dashboard['subscription']}")
    
    # Analytics
    print("\n📈 Platform Analytics:")
    analytics = PlatformAnalytics(platform)
    stats = analytics.get_platform_stats()
    print(f"   Total Users: {stats['total_users']}")
    print(f"   Active Users: {stats['active_users']}")
    
    print("\n✨ Features:")
    print("   - User account management")
    print("   - Individual dashboards")
    print("   - Opportunity tracking")
    print("   - Proposal management")
    print("   - Notification system")
    print("   - Subscription tiers")
    print("   - Platform analytics")
