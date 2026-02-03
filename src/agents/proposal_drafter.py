"""
Proposal Drafter Agent

Generates tailored proposals for opportunities using LLM.
Creates multiple variants with different tones/emphasis for A/B testing.
Integrates with Opik for experiment tracking.
"""

import json
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class ProposalTone(Enum):
    """Different tones for proposal generation"""
    FORMAL = "formal"  # Academic, professional
    ENGAGING = "engaging"  # Conversational, personal
    IMPACT_DRIVEN = "impact_driven"  # Focus on outcomes & community


@dataclass
class ProposalDraft:
    """Represents a generated proposal draft"""
    opportunity_id: str
    user_id: str
    content: str
    tone: ProposalTone
    word_count: int
    generated_at: str
    version: int = 1


class ProposalDrafter:
    """
    Drafter Agent: Generates tailored proposals for opportunities.
    
    This agent:
    1. Analyzes opportunity requirements
    2. Retrieves user profile & achievements
    3. Generates initial draft(s) in specified tone(s)
    4. Supports multiple output formats (proposal, artist statement, CV section)
    5. Stores versions for provenance tracking
    """
    
    def __init__(self, name: str = "Proposal Drafter"):
        self.name = name
        self.tone_templates = self._load_tone_templates()
    
    def _load_tone_templates(self) -> Dict[ProposalTone, str]:
        """Load tone-specific prompt templates"""
        templates = {
            ProposalTone.FORMAL: """
Generate a formal, professional proposal with these characteristics:
- Academic tone and vocabulary
- Emphasis on credentials and proven track record
- Clear structure with sections: Background, Relevance, Deliverables, Impact
- Professional formatting
            """,
            ProposalTone.ENGAGING: """
Generate an engaging, conversational proposal with these characteristics:
- Warm, accessible tone
- Personal anecdotes and human connection
- Emphasis on genuine passion and values
- Conversational structure that draws reader in
            """,
            ProposalTone.IMPACT_DRIVEN: """
Generate an impact-focused proposal with these characteristics:
- Lead with problem/opportunity and intended impact
- Emphasize community benefit and social value
- Quantified metrics and measurable outcomes
- Clear connection between user's work and organizational mission
            """
        }
        return templates
    
    def generate_proposal(
        self,
        user_profile: dict,
        opportunity: dict,
        tone: ProposalTone = ProposalTone.ENGAGING,
        proposal_type: str = "general"
    ) -> ProposalDraft:
        """
        Generate a proposal draft for an opportunity.
        
        Args:
            user_profile: User's profile data
            opportunity: Opportunity details
            tone: Tone/style for the proposal
            proposal_type: Type of proposal ("general", "artist_statement", "cv_section")
            
        Returns:
            ProposalDraft object
        """
        logger.info(f"Drafter Agent: Generating {tone.value} proposal for {opportunity.get('title', 'Unknown')}")
        
        # In a real implementation, this would call OpenAI/Claude API
        # For MVP, we'll use a template-based approach
        draft_content = self._generate_draft_content(
            user_profile,
            opportunity,
            tone,
            proposal_type
        )
        
        draft = ProposalDraft(
            opportunity_id=opportunity.get("id", "unknown"),
            user_id=user_profile.get("user_id", "unknown"),
            content=draft_content,
            tone=tone,
            word_count=len(draft_content.split()),
            generated_at=self._get_timestamp()
        )
        
        return draft
    
    def generate_proposal_variants(
        self,
        user_profile: dict,
        opportunity: dict,
        num_variants: int = 3
    ) -> List[ProposalDraft]:
        """
        Generate multiple proposal variants with different tones.
        
        Args:
            user_profile: User's profile data
            opportunity: Opportunity details
            num_variants: Number of variants to generate
            
        Returns:
            List of ProposalDraft objects
        """
        logger.info(f"Drafter Agent: Generating {num_variants} proposal variants")
        
        tones = [ProposalTone.FORMAL, ProposalTone.ENGAGING, ProposalTone.IMPACT_DRIVEN]
        tones = tones[:num_variants]
        
        variants = []
        for tone in tones:
            variant = self.generate_proposal(user_profile, opportunity, tone)
            variants.append(variant)
        
        return variants
    
    def _generate_draft_content(
        self,
        user_profile: dict,
        opportunity: dict,
        tone: ProposalTone,
        proposal_type: str
    ) -> str:
        """
        Generate draft content using template logic.
        
        In production, this would use LLM API (OpenAI, Anthropic, etc.)
        For MVP, we use structured templates to demonstrate the concept.
        """
        
        name = user_profile.get("name", "Creative Professional")
        bio = user_profile.get("bio", "")
        achievements = user_profile.get("achievements", [])
        interests = user_profile.get("interests", [])
        
        opp_title = opportunity.get("title", "")
        opp_org = opportunity.get("organization", "")
        opp_desc = opportunity.get("description", "")
        opp_requirements = opportunity.get("requirements", [])
        
        # Construct proposal based on tone
        if tone == ProposalTone.FORMAL:
            content = f"""
PROPOSAL FOR: {opp_title}
Organization: {opp_org}

1. BACKGROUND & QUALIFICATIONS

{name} is a creative professional with {len(achievements)} years of professional accomplishments, 
including:
{chr(10).join(f"• {a}" for a in achievements)}

Current focus areas: {", ".join(interests)}

2. PROJECT/PRESENTATION OVERVIEW

This proposal addresses the opportunity to {opp_title.lower()} within the context of {opp_org}.

{bio}

3. ALIGNMENT WITH REQUIREMENTS

This proposal specifically addresses the following organizational requirements:
{chr(10).join(f"• {req}: {name}'s work directly engages with this requirement" for req in opp_requirements[:3])}

4. EXPECTED OUTCOMES

- Delivery of high-quality work aligned with organizational standards
- Demonstrated expertise in {interests[0] if interests else 'creative practice'}
- Positive contribution to {opp_org}'s mission and community

5. CONCLUSION

{name} is positioned to make a meaningful contribution to this initiative and looks 
forward to collaboration with {opp_org}.
            """
        
        elif tone == ProposalTone.ENGAGING:
            content = f"""
A Proposal from {name}

---

Hi there! I'm {name}, and I'm excited about the opportunity to contribute to {opp_org}.

Why? Because {interests[0] if interests else 'creative work'} is what drives me. Over the years, 
I've had the privilege of:
{chr(10).join(f"✦ {a}" for a in achievements)}

When I saw the call for {opp_title.lower()}, I immediately thought about how my background in 
{interests[0] if interests else 'the arts'} could serve {opp_org}'s mission.

Here's what I'd bring:
{chr(10).join(f"→ {req.capitalize()}" for req in opp_requirements[:3])}

But beyond the checklist, here's the real story: {bio}

I believe that {interests[0] if interests else 'creative practice'} has the power to shift 
perspectives and build community. I'd be honored to explore that possibility with {opp_org}.

Let's create something meaningful together.

— {name}
            """
        
        else:  # IMPACT_DRIVEN
            content = f"""
PROPOSAL: {opp_title}
Submitted by: {name}

THE PROBLEM / OPPORTUNITY

{opp_org} has identified the need for {opp_title.lower()}. This represents a critical opportunity 
to advance the mission of {opp_org}.

WHY {name}?

{name} brings {len(achievements)} documented successes in this space:
{chr(10).join(f"⊕ {a}" for a in achievements)}

THE APPROACH

By leveraging expertise in {", ".join(interests[:2])}, this proposal will:
1. Address core organizational requirements: {", ".join(opp_requirements[:2])}
2. Deliver measurable impact in: {interests[0] if interests else 'community engagement'}
3. Create sustainable value for {opp_org} and its stakeholders

EXPECTED IMPACT

- Quantified improvement in mission alignment
- Enhanced visibility and reach for {opp_org}
- Demonstration of innovative practice in {interests[0] if interests else 'the field'}

CONCLUSION

{name} is uniquely positioned to deliver on this opportunity and drive meaningful change.
            """
        
        return content.strip()
    
    def refine_draft(
        self,
        draft: ProposalDraft,
        user_feedback: str
    ) -> ProposalDraft:
        """
        Refine a draft based on user feedback.
        
        Args:
            draft: Original draft
            user_feedback: User's feedback/revisions
            
        Returns:
            Refined ProposalDraft
        """
        logger.info(f"Drafter Agent: Refining proposal based on user feedback")
        
        # In production, would use LLM for intelligent refinement
        refined_content = draft.content + f"\n\n[USER FEEDBACK INCORPORATED]: {user_feedback}"
        
        refined = ProposalDraft(
            opportunity_id=draft.opportunity_id,
            user_id=draft.user_id,
            content=refined_content,
            tone=draft.tone,
            word_count=len(refined_content.split()),
            generated_at=self._get_timestamp(),
            version=draft.version + 1
        )
        
        return refined
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    drafter = ProposalDrafter()
    
    # Sample user and opportunity
    user = {
        "user_id": "user_001",
        "name": "Alex Chen",
        "bio": "Visual artist and creative technologist exploring AI and human connection.",
        "achievements": [
            "Solo exhibition at MoMA PS1 (2024)",
            "Eyebeam Art & Technology Residency (2023)",
            "Speaker at SXSW Interactive (2023)"
        ],
        "interests": ["AI ethics", "generative art", "creative coding"]
    }
    
    opportunity = {
        "id": "opp_001",
        "title": "TED-style Talk on AI in Arts",
        "organization": "CreativeAI Summit 2026",
        "description": "Speakers on the intersection of AI and creative practice",
        "requirements": [
            "Prior speaking experience",
            "Expertise in AI and creativity",
            "Ability to articulate vision"
        ]
    }
    
    # Generate variants
    print("\n=== Generating Proposal Variants ===\n")
    variants = drafter.generate_proposal_variants(user, opportunity, num_variants=3)
    
    for i, variant in enumerate(variants, 1):
        print(f"\n--- Variant {i}: {variant.tone.value.upper()} ---")
        print(variant.content)
        print(f"\nWord count: {variant.word_count}")
        print("-" * 60)
