"""
DAO Connector

Manages interactions with Decentralized Autonomous Organization (DAO) governance.
Enables community voting on opportunities and proposals.
Tracks DAO treasury and token economics.
"""

import logging
import json
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class DAOProposal:
    """A proposal for DAO voting"""
    proposal_id: str
    title: str
    description: str
    creator_address: str
    vote_start: str  # ISO timestamp
    vote_end: str
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    status: str = "pending"  # pending, active, passed, failed, executed


@dataclass
class DAOMember:
    """DAO member with voting power"""
    member_address: str
    voting_power: float  # Number of tokens
    reputation_score: float  # 0.0 to 1.0
    joined_at: str


class DAOConnector:
    """
    DAO Connector: Manage decentralized governance.
    
    This component:
    1. Creates proposals for community voting
    2. Tracks voting on opportunities and strategies
    3. Manages DAO treasury and token economics
    4. Enables decentralized decision-making
    5. Records voting history and outcomes
    
    Note: This is a simulation for MVP. Production would interact with 
    blockchain (Ethereum, Polygon, etc.)
    """
    
    def __init__(self, name: str = "DAO Connector"):
        self.name = name
        self.proposals: Dict[str, DAOProposal] = {}
        self.members: Dict[str, DAOMember] = {}
        self.voting_records: List[Dict] = []
        self.treasury_balance = 10000  # Initial treasury
    
    def register_member(
        self,
        member_address: str,
        initial_voting_power: float,
        reputation_score: float = 0.5
    ) -> DAOMember:
        """
        Register a new DAO member.
        
        Args:
            member_address: Blockchain address of member
            initial_voting_power: Initial token balance
            reputation_score: Initial reputation (0.0-1.0)
            
        Returns:
            DAOMember object
        """
        logger.info(f"DAO Connector: Registering member {member_address[:8]}...")
        
        member = DAOMember(
            member_address=member_address,
            voting_power=initial_voting_power,
            reputation_score=reputation_score,
            joined_at=datetime.now().isoformat()
        )
        
        self.members[member_address] = member
        logger.info(f"  ✓ Member registered with {initial_voting_power} voting power")
        
        return member
    
    def create_proposal(
        self,
        title: str,
        description: str,
        creator_address: str,
        voting_period_hours: int = 72
    ) -> DAOProposal:
        """
        Create a new DAO proposal.
        
        Args:
            title: Proposal title
            description: Detailed description
            creator_address: Address of proposal creator
            voting_period_hours: How long voting lasts
            
        Returns:
            DAOProposal object
        """
        logger.info(f"DAO Connector: Creating proposal: {title}")
        
        from datetime import timedelta
        now = datetime.now()
        
        proposal_id = f"prop_{now.timestamp()}"
        
        proposal = DAOProposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            creator_address=creator_address,
            vote_start=now.isoformat(),
            vote_end=(now + timedelta(hours=voting_period_hours)).isoformat(),
            status="active"
        )
        
        self.proposals[proposal_id] = proposal
        logger.info(f"  ✓ Proposal created: {proposal_id}")
        
        return proposal
    
    def cast_vote(
        self,
        proposal_id: str,
        voter_address: str,
        vote: str  # "for", "against", "abstain"
    ) -> bool:
        """
        Cast a vote on a proposal.
        
        Args:
            proposal_id: ID of proposal
            voter_address: Address of voter
            vote: Vote choice
            
        Returns:
            True if vote was recorded
        """
        if proposal_id not in self.proposals:
            logger.warning(f"DAO Connector: Proposal {proposal_id} not found")
            return False
        
        if voter_address not in self.members:
            logger.warning(f"DAO Connector: Voter {voter_address[:8]}... not a member")
            return False
        
        proposal = self.proposals[proposal_id]
        voter = self.members[voter_address]
        
        if proposal.status != "active":
            logger.warning(f"DAO Connector: Proposal {proposal_id} is not active")
            return False
        
        # Record vote
        voting_power = voter.voting_power
        
        if vote == "for":
            proposal.votes_for += voting_power
        elif vote == "against":
            proposal.votes_against += voting_power
        elif vote == "abstain":
            proposal.votes_abstain += voting_power
        else:
            return False
        
        # Record in history
        self.voting_records.append({
            "proposal_id": proposal_id,
            "voter": voter_address,
            "vote": vote,
            "power": voting_power,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"DAO Connector: Vote recorded for {proposal_id}")
        return True
    
    def finalize_vote(self, proposal_id: str) -> Dict:
        """
        Finalize voting on a proposal and determine outcome.
        
        Args:
            proposal_id: ID of proposal
            
        Returns:
            Voting result summary
        """
        if proposal_id not in self.proposals:
            return {}
        
        proposal = self.proposals[proposal_id]
        
        # Check if voting period is over
        vote_end = datetime.fromisoformat(proposal.vote_end)
        if datetime.now() < vote_end:
            logger.warning(f"DAO Connector: Voting period for {proposal_id} not ended yet")
            return {}
        
        # Determine outcome
        total_votes = proposal.votes_for + proposal.votes_against + proposal.votes_abstain
        
        if proposal.votes_for > proposal.votes_against:
            proposal.status = "passed"
        else:
            proposal.status = "failed"
        
        result = {
            "proposal_id": proposal_id,
            "title": proposal.title,
            "status": proposal.status,
            "votes_for": proposal.votes_for,
            "votes_against": proposal.votes_against,
            "votes_abstain": proposal.votes_abstain,
            "total_votes": total_votes,
            "pass_threshold": 50.0,
            "approval_percentage": (proposal.votes_for / total_votes * 100) if total_votes > 0 else 0
        }
        
        logger.info(f"DAO Connector: Proposal {proposal_id} finalized: {proposal.status}")
        
        return result
    
    def create_opportunity_proposal(
        self,
        opportunity_id: str,
        opportunity_title: str,
        opportunity_description: str,
        creator_address: str
    ) -> DAOProposal:
        """
        Create a DAO proposal to validate a new opportunity.
        
        Args:
            opportunity_id: ID of the opportunity
            opportunity_title: Title of opportunity
            opportunity_description: Description
            creator_address: Address of proposal creator
            
        Returns:
            DAOProposal object
        """
        description = f"""
Should CuratAI recommend the following opportunity?

**Opportunity**: {opportunity_title}

{opportunity_description}

Vote to approve this opportunity for inclusion in the CuratAI system.
        """
        
        return self.create_proposal(
            title=f"Approve Opportunity: {opportunity_title}",
            description=description,
            creator_address=creator_address
        )
    
    def get_member_info(self, member_address: str) -> Optional[Dict]:
        """Get information about a member"""
        if member_address not in self.members:
            return None
        
        member = self.members[member_address]
        return {
            "address": member.member_address,
            "voting_power": member.voting_power,
            "reputation": f"{member.reputation_score:.0%}",
            "joined": member.joined_at
        }
    
    def get_governance_stats(self) -> Dict:
        """Get overall DAO governance statistics"""
        active_proposals = sum(1 for p in self.proposals.values() if p.status == "active")
        passed_proposals = sum(1 for p in self.proposals.values() if p.status == "passed")
        
        total_voting_power = sum(m.voting_power for m in self.members.values())
        
        stats = {
            "total_members": len(self.members),
            "total_voting_power": total_voting_power,
            "treasury_balance": self.treasury_balance,
            "total_proposals": len(self.proposals),
            "active_proposals": active_proposals,
            "passed_proposals": passed_proposals,
            "total_votes_cast": len(self.voting_records)
        }
        
        return stats


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    dao = DAOConnector()
    
    # Register members
    print("\n=== Registering DAO Members ===\n")
    
    dao.register_member("0x1111...1111", 1000, 0.8)
    dao.register_member("0x2222...2222", 500, 0.7)
    dao.register_member("0x3333...3333", 250, 0.6)
    
    # Create a proposal
    print("\n=== Creating Proposal ===\n")
    
    proposal = dao.create_proposal(
        title="Approve TED-style Talk Opportunity",
        description="""
        This proposal recommends including "TED-style Talk on AI in Arts" 
        as a high-priority opportunity for CuratAI members.
        """,
        creator_address="0x1111...1111"
    )
    
    # Cast votes
    print("\n=== Casting Votes ===\n")
    
    dao.cast_vote(proposal.proposal_id, "0x1111...1111", "for")
    dao.cast_vote(proposal.proposal_id, "0x2222...2222", "for")
    dao.cast_vote(proposal.proposal_id, "0x3333...3333", "against")
    
    # Show voting results
    print("\n=== Voting Results ===\n")
    result = dao.finalize_vote(proposal.proposal_id)
    print(json.dumps(result, indent=2))
    
    # Show DAO stats
    print("\n=== DAO Governance Stats ===\n")
    stats = dao.get_governance_stats()
    print(json.dumps(stats, indent=2))
