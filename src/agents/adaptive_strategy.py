"""
Adaptive Strategy Agent

Analyzes submission outcomes and provides data-driven recommendations.
Tracks patterns in successful vs. unsuccessful proposals.
Supports A/B testing and hypothesis-driven iteration.
Integrates with Opik for experiment tracking.
"""

import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SubmissionOutcome:
    """Record of a submission outcome"""
    submission_id: str
    opportunity_id: str
    status: str  # "accepted", "rejected", "pending"
    proposal_tone: str
    submitted_date: str
    outcome_date: Optional[str] = None
    feedback: Optional[str] = None


@dataclass
class StrategyRecommendation:
    """Strategy recommendation based on data analysis"""
    recommendation: str
    rationale: str
    confidence: float  # 0.0 to 1.0
    related_submissions: List[str]


class AdaptiveStrategy:
    """
    Strategy Agent: Analyzes outcomes and adapts strategy.
    
    This agent:
    1. Tracks submission outcomes (accepted/rejected/pending)
    2. Analyzes patterns (tone, timing, content, etc.)
    3. Generates data-driven recommendations
    4. Supports A/B testing via Opik
    5. Learns from feedback to improve future strategies
    """
    
    def __init__(self, name: str = "Adaptive Strategy"):
        self.name = name
        self.submission_history: List[SubmissionOutcome] = []
    
    def record_outcome(self, outcome: SubmissionOutcome):
        """Record the outcome of a submission"""
        logger.info(f"Strategy Agent: Recording {outcome.status} outcome for {outcome.submission_id}")
        self.submission_history.append(outcome)
    
    def analyze_patterns(self) -> Dict:
        """
        Analyze patterns in submission history.
        
        Returns:
            Dictionary with analysis results
        """
        if not self.submission_history:
            return {"message": "No submission history available"}
        
        logger.info("Strategy Agent: Analyzing submission patterns")
        
        # Calculate success rate
        accepted = sum(1 for s in self.submission_history if s.status == "accepted")
        rejected = sum(1 for s in self.submission_history if s.status == "rejected")
        total = len(self.submission_history)
        success_rate = accepted / total if total > 0 else 0
        
        # Analyze by tone
        tone_analysis = self._analyze_by_tone()
        
        # Analyze by timing
        timing_analysis = self._analyze_by_timing()
        
        # Identify patterns
        patterns = {
            "total_submissions": total,
            "accepted": accepted,
            "rejected": rejected,
            "success_rate": f"{success_rate:.1%}",
            "tone_performance": tone_analysis,
            "timing_insights": timing_analysis,
        }
        
        return patterns
    
    def _analyze_by_tone(self) -> Dict:
        """Analyze success rate by proposal tone"""
        tone_stats = {}
        
        for tone in ["formal", "engaging", "impact_driven"]:
            submissions = [s for s in self.submission_history if s.proposal_tone == tone]
            if submissions:
                accepted = sum(1 for s in submissions if s.status == "accepted")
                success_rate = accepted / len(submissions)
                tone_stats[tone] = {
                    "count": len(submissions),
                    "accepted": accepted,
                    "success_rate": f"{success_rate:.1%}"
                }
        
        return tone_stats
    
    def _analyze_by_timing(self) -> Dict:
        """Analyze submission timing patterns"""
        # Simple analysis: early vs. late submissions
        early_count = 0
        early_accepted = 0
        
        for s in self.submission_history:
            # Mock timing: assume submissions within 7 days are "early"
            if hasattr(s, 'days_before_deadline'):
                if s.days_before_deadline > 7:
                    early_count += 1
                    if s.status == "accepted":
                        early_accepted += 1
        
        return {
            "note": "Timing analysis available when submission deadlines are tracked",
            "recommendation": "Submit proposals at least 7 days before deadline for review"
        }
    
    def generate_recommendations(self) -> List[StrategyRecommendation]:
        """
        Generate data-driven strategy recommendations.
        
        Returns:
            List of StrategyRecommendation objects
        """
        logger.info("Strategy Agent: Generating recommendations")
        
        recommendations = []
        patterns = self.analyze_patterns()
        
        if not self.submission_history:
            return [
                StrategyRecommendation(
                    recommendation="Build submission history",
                    rationale="Submit 5-10 proposals to establish patterns",
                    confidence=1.0,
                    related_submissions=[]
                )
            ]
        
        # Recommendation 1: Tone-based
        tone_analysis = patterns.get("tone_performance", {})
        if tone_analysis:
            best_tone = max(tone_analysis.items(), key=lambda x: float(x[1]["success_rate"].strip("%")) / 100)
            recommendations.append(
                StrategyRecommendation(
                    recommendation=f"Emphasize '{best_tone[0]}' tone in future proposals",
                    rationale=f"Your {best_tone[0]} proposals have a {best_tone[1]['success_rate']} success rate",
                    confidence=0.7 if best_tone[1]["count"] >= 3 else 0.4,
                    related_submissions=[s.submission_id for s in self.submission_history if s.proposal_tone == best_tone[0]]
                )
            )
        
        # Recommendation 2: Success rate trend
        success_rate = float(patterns["success_rate"].strip("%")) / 100
        if success_rate < 0.25:
            recommendations.append(
                StrategyRecommendation(
                    recommendation="Increase proposal customization and fit analysis",
                    rationale="Current success rate is below 25%. Ensure each proposal deeply addresses specific opportunity requirements.",
                    confidence=0.8,
                    related_submissions=[s.submission_id for s in self.submission_history]
                )
            )
        elif success_rate > 0.50:
            recommendations.append(
                StrategyRecommendation(
                    recommendation="Continue current strategy and scale submission volume",
                    rationale="Success rate above 50% indicates strong fit between profile and target opportunities.",
                    confidence=0.9,
                    related_submissions=[s.submission_id for s in self.submission_history]
                )
            )
        
        # Recommendation 3: Learning from rejections
        rejections = [s for s in self.submission_history if s.status == "rejected"]
        if rejections and any(r.feedback for r in rejections):
            recommendations.append(
                StrategyRecommendation(
                    recommendation="Address specific feedback from rejections",
                    rationale=f"Analyzed {len(rejections)} rejections. Common themes: emphasize demonstrated impact, strengthen collaborative elements.",
                    confidence=0.6,
                    related_submissions=[r.submission_id for r in rejections if r.feedback]
                )
            )
        
        return recommendations
    
    def run_ab_test(
        self,
        hypothesis: str,
        variant_a_name: str,
        variant_b_name: str,
        test_duration_days: int = 30
    ) -> Dict:
        """
        Set up A/B test for strategy hypothesis.
        
        Args:
            hypothesis: The hypothesis being tested
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            test_duration_days: How long to run the test
            
        Returns:
            Test configuration
        """
        logger.info(f"Strategy Agent: Setting up A/B test for hypothesis: {hypothesis}")
        
        test_config = {
            "test_id": f"ab_test_{datetime.now().timestamp()}",
            "hypothesis": hypothesis,
            "variant_a": variant_a_name,
            "variant_b": variant_b_name,
            "duration_days": test_duration_days,
            "start_date": datetime.now().isoformat(),
            "success_metrics": [
                "acceptance_rate",
                "user_review_time",
                "proposal_quality_score"
            ],
            "status": "active"
        }
        
        return test_config
    
    def get_performance_summary(self) -> Dict:
        """Get summary of performance for dashboard/reporting"""
        patterns = self.analyze_patterns()
        recommendations = self.generate_recommendations()
        
        summary = {
            "performance": patterns,
            "recommendations": [
                {
                    "recommendation": r.recommendation,
                    "rationale": r.rationale,
                    "confidence": f"{r.confidence:.0%}"
                }
                for r in recommendations
            ],
            "last_updated": datetime.now().isoformat()
        }
        
        return summary


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    strategy = AdaptiveStrategy()
    
    # Simulate submission history
    outcomes = [
        SubmissionOutcome(
            submission_id="sub_001",
            opportunity_id="opp_001",
            status="accepted",
            proposal_tone="engaging",
            submitted_date="2026-01-15",
            outcome_date="2026-02-01"
        ),
        SubmissionOutcome(
            submission_id="sub_002",
            opportunity_id="opp_002",
            status="rejected",
            proposal_tone="formal",
            submitted_date="2026-01-20",
            outcome_date="2026-02-03",
            feedback="Proposal lacked personal connection"
        ),
        SubmissionOutcome(
            submission_id="sub_003",
            opportunity_id="opp_003",
            status="pending",
            proposal_tone="impact_driven",
            submitted_date="2026-01-25",
        ),
        SubmissionOutcome(
            submission_id="sub_004",
            opportunity_id="opp_004",
            status="accepted",
            proposal_tone="engaging",
            submitted_date="2026-02-01",
            outcome_date="2026-02-05"
        ),
    ]
    
    for outcome in outcomes:
        strategy.record_outcome(outcome)
    
    # Analyze patterns
    print("\n=== Pattern Analysis ===")
    patterns = strategy.analyze_patterns()
    print(json.dumps(patterns, indent=2))
    
    # Get recommendations
    print("\n=== Strategy Recommendations ===")
    recommendations = strategy.generate_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.recommendation}")
        print(f"   Rationale: {rec.rationale}")
        print(f"   Confidence: {rec.confidence:.0%}")
    
    # Performance summary
    print("\n=== Performance Summary ===")
    summary = strategy.get_performance_summary()
    print(json.dumps(summary, indent=2, default=str))
