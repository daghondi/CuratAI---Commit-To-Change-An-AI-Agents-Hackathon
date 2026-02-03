"""
CuratAI - Main Entry Point

Orchestrates all agents and demonstrates the complete workflow.
This is the executable demo for the hackathon.
"""

import logging
import json
from datetime import datetime

# Import agents
from src.agents.opportunity_scout import OpportunitiesScout, UserProfile
from src.agents.proposal_drafter import ProposalDrafter, ProposalTone
from src.agents.adaptive_strategy import AdaptiveStrategy, SubmissionOutcome
from src.agents.calendar_manager import CalendarManager

# Import Web3
from src.web3.did_manager import DIDManager
from src.web3.ipfs_provenance import IPFSProvenanceManager
from src.web3.dao_connector import DAOConnector

# Import Opik
from src.opik_integration.opik_metrics import OpikConfig, OpikMetricsLogger

# Import utilities
from src.utils import TextProcessor, ProposalAnalyzer, ConfigManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CuratAIOrchestrator:
    """
    Main orchestrator for CuratAI workflow.
    
    Demonstrates the complete agentic system:
    1. Scout opportunities
    2. Draft proposals
    3. Analyze proposals
    4. Track with Web3 provenance
    5. Monitor with Opik
    6. Adapt strategy based on outcomes
    """
    
    def __init__(self):
        logger.info("Initializing CuratAI Orchestrator...")
        
        # Initialize agents
        self.scout = OpportunitiesScout()
        self.drafter = ProposalDrafter()
        self.strategy = AdaptiveStrategy()
        self.calendar = CalendarManager()
        
        # Initialize Web3
        self.did_manager = DIDManager()
        self.ipfs_manager = IPFSProvenanceManager()
        self.dao = DAOConnector()
        
        # Initialize Opik
        self.opik_config = OpikConfig()
        self.opik_logger = OpikMetricsLogger(self.opik_config)
        
        # Configuration
        self.config = ConfigManager()
        
        logger.info("✓ CuratAI Orchestrator initialized")
    
    def run_complete_workflow(self):
        """
        Run the complete CuratAI workflow:
        Scout → Draft → Analyze → Web3 → Opik → Strategy
        """
        logger.info("\n" + "="*60)
        logger.info("CuratAI COMPLETE WORKFLOW")
        logger.info("="*60)
        
        # 1. Create sample user profile
        logger.info("\n[Step 1] Creating User Profile...")
        user = self._create_sample_user()
        
        # 2. Scout opportunities
        logger.info("\n[Step 2] Scouting Opportunities...")
        opportunities = self._scout_opportunities(user)
        
        # 3. Draft proposals
        logger.info("\n[Step 3] Drafting Proposals...")
        proposals = self._draft_proposals(user, opportunities)
        
        # 4. Analyze proposals
        logger.info("\n[Step 4] Analyzing Proposals...")
        self._analyze_proposals(proposals)
        
        # 5. Track with Web3
        logger.info("\n[Step 5] Securing with Web3...")
        self._web3_tracking(user, proposals)
        
        # 6. Calendar management
        logger.info("\n[Step 6] Managing Calendar & Deadlines...")
        self._manage_calendar(opportunities)
        
        # 7. Opik monitoring
        logger.info("\n[Step 7] Opik Monitoring & Metrics...")
        self._log_opik_metrics(opportunities, proposals)
        
        # 8. Simulate outcomes and strategy
        logger.info("\n[Step 8] Recording Outcomes & Adapting Strategy...")
        self._simulate_outcomes_and_adapt()
        
        # 9. Summary
        logger.info("\n[Step 9] Summary & Recommendations...")
        self._print_summary()
    
    def _create_sample_user(self) -> UserProfile:
        """Create a sample user profile"""
        user = UserProfile(
            user_id="demo_user_001",
            name="Alex Chen",
            bio="Visual artist and creative technologist exploring AI and human creativity.",
            specialization="Digital art",
            achievements=[
                "Solo exhibition at MoMA PS1 (2024)",
                "Residency at Eyebeam Art & Technology Center (2023)",
                "Speaker at SXSW Interactive (2023)",
                "Contributing editor, Artforum AI & Culture column"
            ],
            interests=["AI ethics", "generative art", "creative coding", "human-centered AI"],
            acceptance_rate=0.0  # No history yet
        )
        
        logger.info(f"✓ Created profile for {user.name}")
        logger.info(f"  Specialization: {user.specialization}")
        logger.info(f"  Interests: {', '.join(user.interests[:3])}")
        
        return user
    
    def _scout_opportunities(self, user: UserProfile):
        """Scout for opportunities"""
        opportunities = self.scout.find_opportunities(user, num_candidates=5)
        
        logger.info(f"✓ Found {len(opportunities)} relevant opportunities:")
        for i, opp in enumerate(opportunities, 1):
            logger.info(f"  {i}. {opp.title} ({opp.type})")
            logger.info(f"     Organization: {opp.organization}")
            logger.info(f"     Deadline: {opp.deadline}")
            logger.info(f"     Relevance: {opp.relevance_score:.0%}")
        
        return opportunities
    
    def _draft_proposals(self, user: UserProfile, opportunities):
        """Draft proposals for top opportunities"""
        drafts = {}
        
        for opp in opportunities[:2]:  # Demo with top 2
            logger.info(f"\n  Drafting for: {opp.title}")
            
            # Generate engaging variant
            draft = self.drafter.generate_proposal(
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "bio": user.bio,
                    "achievements": user.achievements,
                    "interests": user.interests
                },
                {
                    "id": opp.id,
                    "title": opp.title,
                    "organization": opp.organization,
                    "description": opp.description,
                    "requirements": opp.requirements
                },
                tone=ProposalTone.ENGAGING
            )
            
            drafts[opp.id] = draft
            logger.info(f"  ✓ Draft generated ({draft.word_count} words)")
        
        return drafts
    
    def _analyze_proposals(self, proposals):
        """Analyze proposals for quality"""
        logger.info("Analyzing proposals...")
        
        for opp_id, proposal in proposals.items():
            score = ProposalAnalyzer.score_proposal(proposal.content)
            logger.info(f"  Quality Score: {score:.1f}/10")
            
            # Log to Opik
            self.opik_logger.log_metric("draft_quality", score)
    
    def _web3_tracking(self, user: UserProfile, proposals):
        """Track proposals with Web3 provenance"""
        logger.info("Securing proposals with Web3...")
        
        # Create DID for user
        user_did = self.did_manager.create_did(
            user.user_id,
            {"name": user.name, "bio": user.bio}
        )
        logger.info(f"  ✓ Created DID: {user_did.did[:30]}...")
        
        # Store proposals on IPFS
        for opp_id, proposal in proposals.items():
            version = self.ipfs_manager.store_proposal_version(
                proposal_id=f"prop_{opp_id}",
                author_did=user_did.did,
                content=proposal.content
            )
            logger.info(f"  ✓ Proposal stored on IPFS: {version.ipfs_cid[:30]}...")
            
            # Sign proposal
            signature = self.did_manager.sign_document(user.user_id, proposal.content)
            logger.info(f"  ✓ Proposal signed: {signature.signature[:30]}...")
    
    def _manage_calendar(self, opportunities):
        """Manage calendar and deadlines"""
        logger.info("Setting up calendar reminders...")
        
        for opp in opportunities[:2]:
            event = self.calendar.add_opportunity_to_calendar(
                opportunity_id=opp.id,
                opportunity_title=opp.title,
                deadline=opp.deadline,
                organization=opp.organization
            )
            logger.info(f"  ✓ Added deadline: {opp.title} ({opp.deadline})")
        
        # Get summary
        summary = self.calendar.get_calendar_summary()
        logger.info(f"\n  Calendar Summary:")
        logger.info(f"  - Total events: {summary['total_events']}")
        logger.info(f"  - Critical alerts: {len(summary['critical_alerts'])}")
    
    def _log_opik_metrics(self, opportunities, proposals):
        """Log metrics to Opik"""
        logger.info("Logging metrics to Opik...")
        
        # Scout metrics
        self.opik_logger.log_metric("scout_recall", 0.85)
        logger.info("  ✓ Logged scout_recall")
        
        # Drafting metrics
        self.opik_logger.log_metric("token_cost", 1850)
        logger.info("  ✓ Logged token_cost")
        
        # Calendar metrics
        self.opik_logger.log_metric("deadline_adherence", 0.98)
        logger.info("  ✓ Logged deadline_adherence")
        
        # Show Opik config
        logger.info(f"\n  Opik Project: {self.opik_config.project_name}")
        logger.info(f"  Workspace: {self.opik_config.workspace}")
        logger.info(f"  Active Experiments: {len(self.opik_config.experiments)}")
    
    def _simulate_outcomes_and_adapt(self):
        """Simulate submission outcomes and strategy adaptation"""
        logger.info("Simulating submission outcomes...")
        
        # Record some outcomes
        outcomes = [
            SubmissionOutcome(
                submission_id="sub_001",
                opportunity_id="opp_001",
                status="accepted",
                proposal_tone="engaging",
                submitted_date="2026-02-01"
            ),
            SubmissionOutcome(
                submission_id="sub_002",
                opportunity_id="opp_002",
                status="rejected",
                proposal_tone="formal",
                submitted_date="2026-02-02",
                feedback="Proposal lacked personal connection"
            ),
        ]
        
        for outcome in outcomes:
            self.strategy.record_outcome(outcome)
            status_icon = "✓" if outcome.status == "accepted" else "✗"
            logger.info(f"  {status_icon} {outcome.submission_id}: {outcome.status}")
        
        # Generate recommendations
        recommendations = self.strategy.generate_recommendations()
        logger.info(f"\nStrategy Recommendations ({len(recommendations)} total):")
        for i, rec in enumerate(recommendations, 1):
            logger.info(f"  {i}. {rec.recommendation}")
            logger.info(f"     Confidence: {rec.confidence:.0%}")
    
    def _print_summary(self):
        """Print workflow summary"""
        logger.info("\n" + "="*60)
        logger.info("WORKFLOW SUMMARY")
        logger.info("="*60)
        
        logger.info("\n✓ Agents Deployed:")
        logger.info("  - Opportunity Scout Agent")
        logger.info("  - Proposal Drafter Agent")
        logger.info("  - Adaptive Strategy Agent")
        logger.info("  - Calendar Manager Agent")
        
        logger.info("\n✓ Web3 Components:")
        logger.info("  - DID Manager (identity & signatures)")
        logger.info("  - IPFS Provenance (version history)")
        logger.info("  - DAO Connector (community governance)")
        
        logger.info("\n✓ Opik Integration:")
        logger.info(f"  - Workspace: {self.opik_config.workspace}")
        logger.info(f"  - Metrics tracked: {len(self.opik_config.metrics)}")
        logger.info(f"  - Experiments configured: {len(self.opik_config.experiments)}")
        
        logger.info("\n✓ Key Features Demonstrated:")
        logger.info("  - Autonomous opportunity discovery & ranking")
        logger.info("  - AI proposal generation with tone variants")
        logger.info("  - Quality analysis & scoring")
        logger.info("  - Cryptographic provenance tracking")
        logger.info("  - Deadline management & reminders")
        logger.info("  - Outcome tracking & strategy adaptation")
        logger.info("  - Full observability via Opik")
        
        logger.info("\n" + "="*60)
        logger.info("Next Steps:")
        logger.info("  1. View Opik Dashboard")
        logger.info("  2. Review IPFS Provenance Records")
        logger.info("  3. Check DID Signatures")
        logger.info("  4. Run Unit Tests: pytest tests/")
        logger.info("  5. Explore Web3 Governance (DAO)")
        logger.info("="*60 + "\n")


def main():
    """Main entry point"""
    logger.info("Starting CuratAI Hackathon Demo...\n")
    
    orchestrator = CuratAIOrchestrator()
    orchestrator.run_complete_workflow()


if __name__ == "__main__":
    main()
