"""
Enhanced DAO Connector with Tokenization & Recognition
Enables decentralized governance with NFT badges and token rewards
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class TokenType(Enum):
    """Types of tokens in the CuratAI DAO"""
    GOVERNANCE = "governance"  # CURAI token - voting rights
    RECOGNITION = "recognition"  # Achievement NFT badges
    UTILITY = "utility"  # Access token for platform features


class BadgeType(Enum):
    """Types of achievement badges (NFTs)"""
    FIRST_SUBMISSION = "first_submission"
    GRANT_WINNER = "grant_winner"
    EXHIBITION_FEATURED = "exhibition_featured"
    PROLIFIC_CREATOR = "prolific_creator"
    COMMUNITY_MENTOR = "community_mentor"
    OPIK_EXCELLENCE = "opik_excellence"
    STRATEGY_MASTER = "strategy_master"


@dataclass
class CurAIToken:
    """
    CurAI Governance Token
    ERC-20 token for DAO voting and platform governance
    """
    token_id: str
    holder_address: str
    token_type: TokenType
    amount: int  # In smallest unit (wei equivalent)
    minted_at: datetime
    expires_at: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'token_id': self.token_id,
            'holder': self.holder_address,
            'type': self.token_type.value,
            'amount': self.amount,
            'minted_at': self.minted_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'metadata': self.metadata
        }


@dataclass
class NFTBadge:
    """
    Achievement NFT Badge
    ERC-721 token representing artist achievements
    """
    badge_id: str
    artist_did: str
    badge_type: BadgeType
    minted_at: datetime
    metadata: Dict = field(default_factory=dict)
    ipfs_hash: Optional[str] = None  # Link to badge artwork/metadata on IPFS
    
    def to_dict(self) -> Dict:
        return {
            'badge_id': self.badge_id,
            'artist_did': self.artist_did,
            'type': self.badge_type.value,
            'minted_at': self.minted_at.isoformat(),
            'ipfs_hash': self.ipfs_hash,
            'metadata': self.metadata
        }


@dataclass
class DAOProposalV2:
    """Enhanced DAO Proposal with tokenomics"""
    proposal_id: str
    title: str
    description: str
    proposer_did: str
    proposal_type: str  # governance, allocation, feature, recognition
    status: str  # draft, voting, executed, rejected
    voting_start: datetime
    voting_end: datetime
    votes_for: int = 0
    votes_against: int = 0
    token_reward: int = 0  # CURAI tokens as incentive
    metadata: Dict = field(default_factory=dict)


class TokenomicsManager:
    """
    Manages token distribution and economic incentives
    """
    
    def __init__(self):
        self.total_supply = 1_000_000_000  # 1B total CURAI tokens
        self.distributed = 0
        self.tokens: Dict[str, CurAIToken] = {}
        self.badges: Dict[str, NFTBadge] = {}
        
        # Token allocation
        self.allocation = {
            'governance': 0.40,  # 40% for governance
            'community_rewards': 0.30,  # 30% for community/artists
            'development': 0.15,  # 15% for dev team
            'treasury': 0.15  # 15% for DAO treasury
        }
    
    def mint_governance_tokens(self, holder_address: str, amount: int,
                               metadata: Dict = None) -> CurAIToken:
        """
        Mint CURAI governance tokens for voting rights
        
        Args:
            holder_address: DID of token holder
            amount: Number of tokens to mint
            metadata: Additional info (reason, proposal_link, etc)
        """
        token_id = str(uuid.uuid4())
        token = CurAIToken(
            token_id=token_id,
            holder_address=holder_address,
            token_type=TokenType.GOVERNANCE,
            amount=amount,
            minted_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self.tokens[token_id] = token
        self.distributed += amount
        
        return token
    
    def mint_recognition_badge(self, artist_did: str, badge_type: BadgeType,
                               metadata: Dict = None, ipfs_hash: str = None) -> NFTBadge:
        """
        Mint NFT badge for artist achievement
        
        Args:
            artist_did: DID of artist
            badge_type: Type of achievement badge
            metadata: Achievement details
            ipfs_hash: Link to badge image/data on IPFS
        """
        badge_id = str(uuid.uuid4())
        badge = NFTBadge(
            badge_id=badge_id,
            artist_did=artist_did,
            badge_type=badge_type,
            minted_at=datetime.now(),
            metadata=metadata or {},
            ipfs_hash=ipfs_hash
        )
        
        self.badges[badge_id] = badge
        return badge
    
    def award_achievement_token(self, artist_did: str, reason: str,
                                token_amount: int = 100) -> CurAIToken:
        """
        Award utility tokens for achievements
        - First submission: 100 tokens
        - Grant acceptance: 500 tokens
        - Exhibition featured: 300 tokens
        - Community mentoring: 200 tokens per mentor session
        """
        return self.mint_governance_tokens(
            holder_address=artist_did,
            amount=token_amount,
            metadata={'reason': reason, 'type': 'achievement'}
        )
    
    def get_holder_balance(self, holder_address: str) -> int:
        """Get total token balance for a holder"""
        total = 0
        for token in self.tokens.values():
            if token.holder_address == holder_address:
                total += token.amount
        return total
    
    def get_holder_badges(self, artist_did: str) -> List[NFTBadge]:
        """Get all badges for an artist"""
        return [badge for badge in self.badges.values() 
                if badge.artist_did == artist_did]


class EnhancedDAOConnector:
    """
    Enhanced DAO with governance tokens and NFT badges
    """
    
    def __init__(self):
        self.members: Dict[str, Dict] = {}
        self.proposals: Dict[str, DAOProposalV2] = {}
        self.tokenomics = TokenomicsManager()
    
    def register_member_with_tokens(self, artist_did: str, artist_name: str,
                                   initial_tokens: int = 1000) -> Dict:
        """
        Register artist as DAO member and award initial tokens
        """
        member = {
            'did': artist_did,
            'name': artist_name,
            'joined_at': datetime.now(),
            'token_balance': 0,
            'badges': [],
            'proposals_created': 0,
            'votes_cast': 0
        }
        
        self.members[artist_did] = member
        
        # Award initial onboarding tokens
        token = self.tokenomics.mint_governance_tokens(
            holder_address=artist_did,
            amount=initial_tokens,
            metadata={'reason': 'membership_onboarding'}
        )
        
        member['token_balance'] = initial_tokens
        return member
    
    def create_recognition_proposal(self, proposer_did: str, artist_did: str,
                                   badge_type: BadgeType, reason: str) -> DAOProposalV2:
        """
        Create proposal to recognize artist achievement with NFT badge
        """
        proposal_id = str(uuid.uuid4())
        proposal = DAOProposalV2(
            proposal_id=proposal_id,
            title=f"Award {badge_type.value} badge to {artist_did}",
            description=reason,
            proposer_did=proposer_did,
            proposal_type='recognition',
            status='voting',
            voting_start=datetime.now(),
            voting_end=datetime.now().replace(day=datetime.now().day + 7),
            token_reward=50,  # Reward for voting
            metadata={'badge_type': badge_type.value, 'artist_did': artist_did}
        )
        
        self.proposals[proposal_id] = proposal
        return proposal
    
    def vote_on_proposal(self, voter_did: str, proposal_id: str, 
                        vote: bool) -> Dict:
        """
        Cast vote on proposal (requires token balance)
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {'error': 'Proposal not found'}
        
        voter_balance = self.tokenomics.get_holder_balance(voter_did)
        if voter_balance < 1:
            return {'error': 'Insufficient tokens to vote'}
        
        if vote:
            proposal.votes_for += voter_balance
        else:
            proposal.votes_against += voter_balance
        
        # Award voting participation token
        self.tokenomics.mint_governance_tokens(
            holder_address=voter_did,
            amount=50,
            metadata={'reason': 'voting_participation', 'proposal': proposal_id}
        )
        
        self.members[voter_did]['votes_cast'] += 1
        
        return {
            'success': True,
            'vote': 'for' if vote else 'against',
            'voter_reward': 50
        }
    
    def finalize_proposal(self, proposal_id: str) -> Dict:
        """
        Finalize voting and execute proposal if passed
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return {'error': 'Proposal not found'}
        
        total_votes = proposal.votes_for + proposal.votes_against
        passed = proposal.votes_for > proposal.votes_against
        
        result = {
            'proposal_id': proposal_id,
            'passed': passed,
            'votes_for': proposal.votes_for,
            'votes_against': proposal.votes_against,
            'total_votes': total_votes
        }
        
        if passed and proposal.proposal_type == 'recognition':
            # Execute badge minting
            artist_did = proposal.metadata['artist_did']
            badge_type = BadgeType[proposal.metadata['badge_type'].upper()]
            
            badge = self.tokenomics.mint_recognition_badge(
                artist_did=artist_did,
                badge_type=badge_type,
                metadata=proposal.metadata
            )
            
            self.members[artist_did]['badges'].append(badge.badge_id)
            result['badge_minted'] = badge.badge_id
        
        proposal.status = 'executed' if passed else 'rejected'
        return result
    
    def get_member_profile(self, artist_did: str) -> Dict:
        """Get complete member profile with tokens and badges"""
        member = self.members.get(artist_did)
        if not member:
            return None
        
        badges = self.tokenomics.get_holder_badges(artist_did)
        balance = self.tokenomics.get_holder_balance(artist_did)
        
        return {
            **member,
            'token_balance': balance,
            'badges': [
                {
                    'id': badge.badge_id,
                    'type': badge.badge_type.value,
                    'minted_at': badge.minted_at.isoformat()
                }
                for badge in badges
            ]
        }


# Demo usage
if __name__ == "__main__":
    print("🏛️  Enhanced DAO with Tokenization")
    print("=" * 60)
    
    dao = EnhancedDAOConnector()
    
    # Register members
    print("\n📝 Registering DAO Members...")
    member1 = dao.register_member_with_tokens(
        "did:example:artist001",
        "Alexandra Chen",
        initial_tokens=1000
    )
    print(f"✅ {member1['name']} joined with {member1['token_balance']} CURAI tokens")
    
    # Create recognition proposal
    print("\n🏆 Creating Recognition Proposal...")
    proposal = dao.create_recognition_proposal(
        proposer_did="did:example:artist001",
        artist_did="did:example:artist001",
        badge_type=BadgeType.GRANT_WINNER,
        reason="Successfully won NEA Creative Innovation Grant"
    )
    print(f"✅ Proposal created: {proposal.title}")
    
    print("\n✨ Features:")
    print("   - CURAI governance tokens (ERC-20)")
    print("   - Achievement NFT badges (ERC-721)")
    print("   - Token-weighted voting")
    print("   - Tokenized incentives")
    print("   - Badge marketplace (Phase 2)")
    print("   - DAO treasury management")
