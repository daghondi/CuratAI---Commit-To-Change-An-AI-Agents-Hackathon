"""
Opportunity Scout Agent

Autonomously searches for and ranks opportunities that match the user's profile.
Integrates with Opik for workflow tracking and monitoring.
"""

import json
import logging
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Opportunity:
    """Represents a professional opportunity (speaking, exhibition, grant, etc.)"""
    id: str
    title: str
    type: str  # "speaking", "exhibition", "grant", "fellowship"
    organization: str
    description: str
    deadline: str
    url: str
    requirements: List[str]
    contact_email: Optional[str] = None
    relevance_score: float = 0.0


@dataclass
class UserProfile:
    """User's creative profile and background"""
    user_id: str
    name: str
    bio: str
    specialization: str
    achievements: List[str]
    interests: List[str]
    past_submissions: List[dict] = None
    acceptance_rate: float = 0.0


class OpportunitiesScout:
    """
    Scout Agent: Finds and ranks opportunities for the user.
    
    This agent:
    1. Scans opportunity sources (mock data, APIs, feeds)
    2. Scores each opportunity against user profile
    3. Returns ranked list of opportunities
    4. Learns from user feedback (future)
    """
    
    def __init__(self, name: str = "Opportunity Scout"):
        self.name = name
        self.opportunities_db = self._load_mock_opportunities()
        
    def _load_mock_opportunities(self) -> List[Opportunity]:
        """Load mock opportunities for demo purposes"""
        mock_data = [
            Opportunity(
                id="opp_001",
                title="TED-style Talk on AI in Arts",
                type="speaking",
                organization="CreativeAI Summit 2026",
                description="We're seeking visionary speakers on the intersection of AI and creative practice.",
                deadline="2026-03-15",
                url="https://example.com/creative-ai-summit",
                requirements=[
                    "Prior speaking experience",
                    "Expertise in AI and creativity",
                    "Ability to articulate vision clearly"
                ],
                contact_email="speakers@creativeaisummit.org"
            ),
            Opportunity(
                id="opp_002",
                title="Digital Arts Exhibition",
                type="exhibition",
                organization="ArtNow Gallery",
                description="Curated exhibition of artists exploring technology and human experience.",
                deadline="2026-04-01",
                url="https://example.com/artnow",
                requirements=[
                    "3-5 completed works",
                    "Artist statement (500 words)",
                    "High-res images"
                ],
                contact_email="submissions@artnow.org"
            ),
            Opportunity(
                id="opp_003",
                title="Creative Innovation Grant",
                type="grant",
                organization="National Endowment for the Arts (NEA)",
                description="$50,000 grant for projects at the intersection of traditional and digital media.",
                deadline="2026-05-30",
                url="https://example.com/nea-grants",
                requirements=[
                    "Project proposal (10 pages max)",
                    "Budget breakdown",
                    "Letters of support",
                    "Evidence of past funding"
                ],
                contact_email="grants@nea.gov"
            ),
            Opportunity(
                id="opp_004",
                title="AI Ethics Fellowship",
                type="fellowship",
                organization="Center for Responsible AI",
                description="1-year fellowship to explore ethical implications of creative AI systems.",
                deadline="2026-06-15",
                url="https://example.com/ai-ethics-fellowship",
                requirements=[
                    "CV",
                    "Research proposal",
                    "3 letters of recommendation",
                    "Writing sample"
                ],
                contact_email="fellows@responsibleai.org"
            ),
            Opportunity(
                id="opp_005",
                title="Artist-in-Residence Program",
                type="residency",
                organization="Code & Canvas Studio",
                description="6-month residency blending code and visual art.",
                deadline="2026-03-30",
                url="https://example.com/code-canvas",
                requirements=[
                    "Portfolio of work",
                    "Project concept for residency",
                    "Availability confirmation"
                ],
                contact_email="residency@codeandcanvas.org"
            ),
        ]
        return mock_data
    
    def find_opportunities(
        self,
        user_profile: UserProfile,
        num_candidates: int = 5,
        opportunity_types: Optional[List[str]] = None
    ) -> List[Opportunity]:
        """
        Find and rank opportunities for the user.
        
        Args:
            user_profile: User's profile
            num_candidates: Number of top opportunities to return
            opportunity_types: Filter by specific types (optional)
            
        Returns:
            List of opportunities ranked by relevance
        """
        logger.info(f"Scout Agent: Searching for opportunities for {user_profile.name}")
        
        # Score opportunities against user profile
        scored_opportunities = []
        for opp in self.opportunities_db:
            # Filter by type if specified
            if opportunity_types and opp.type not in opportunity_types:
                continue
                
            score = self._calculate_relevance_score(user_profile, opp)
            opp.relevance_score = score
            scored_opportunities.append(opp)
        
        # Sort by relevance score (descending)
        ranked = sorted(scored_opportunities, key=lambda x: x.relevance_score, reverse=True)
        
        # Return top N
        top_opportunities = ranked[:num_candidates]
        logger.info(f"Scout Agent: Found {len(top_opportunities)} relevant opportunities")
        
        return top_opportunities
    
    def _calculate_relevance_score(self, profile: UserProfile, opportunity: Opportunity) -> float:
        """
        Calculate relevance score between user profile and opportunity.
        
        Scoring factors:
        - Bio/description match with opportunity description
        - Specialization match with opportunity requirements
        - Interest alignment
        - Past success in similar opportunities
        
        Args:
            profile: User profile
            opportunity: Opportunity to score
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        weights = {
            "bio_match": 0.25,
            "specialization_match": 0.25,
            "interest_match": 0.25,
            "past_success": 0.25
        }
        
        # 1. Bio/description match (simple keyword overlap)
        bio_keywords = set(profile.bio.lower().split())
        opp_keywords = set(opportunity.description.lower().split())
        bio_match = len(bio_keywords & opp_keywords) / max(len(bio_keywords), 1)
        
        # 2. Specialization match
        specialization_match = 1.0 if profile.specialization.lower() in opportunity.description.lower() else 0.5
        
        # 3. Interest alignment
        interest_match = sum(
            1 for interest in profile.interests
            if interest.lower() in opportunity.description.lower()
        ) / max(len(profile.interests), 1)
        
        # 4. Past success (if available)
        past_success = profile.acceptance_rate if profile.acceptance_rate > 0 else 0.5
        
        # Weighted sum
        score = (
            weights["bio_match"] * min(bio_match, 1.0) +
            weights["specialization_match"] * specialization_match +
            weights["interest_match"] * min(interest_match, 1.0) +
            weights["past_success"] * past_success
        )
        
        return score
    
    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Opportunity]:
        """Retrieve a specific opportunity by ID"""
        for opp in self.opportunities_db:
            if opp.id == opportunity_id:
                return opp
        return None
    
    def log_feedback(self, opportunity_id: str, feedback: str):
        """Log user feedback on an opportunity for learning"""
        logger.info(f"Scout Agent: Received feedback on {opportunity_id}: {feedback}")
        # In future, this will be used to improve scoring
        pass


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    scout = OpportunitiesScout()
    
    # Create sample user
    user = UserProfile(
        user_id="user_001",
        name="Alex Chen",
        bio="Visual artist and creative technologist exploring the intersection of AI and human creativity.",
        specialization="Digital art",
        achievements=[
            "Solo exhibition at MoMA PS1",
            "Residency at Eyebeam Art & Technology",
            "Speaker at SXSW Interactive"
        ],
        interests=["AI ethics", "generative art", "creative coding", "decentralized systems"],
        acceptance_rate=0.35
    )
    
    # Find opportunities
    opportunities = scout.find_opportunities(user, num_candidates=5)
    
    print("\n=== Top Opportunities for", user.name, "===\n")
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp.title}")
        print(f"   Organization: {opp.organization}")
        print(f"   Type: {opp.type}")
        print(f"   Deadline: {opp.deadline}")
        print(f"   Relevance Score: {opp.relevance_score:.2%}")
        print()
