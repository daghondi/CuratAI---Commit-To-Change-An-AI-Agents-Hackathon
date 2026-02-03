"""
Unit tests for agent modules
"""

import unittest
from src.agents.opportunity_scout import OpportunitiesScout, UserProfile


class TestOpportunitiesScout(unittest.TestCase):
    """Tests for Opportunity Scout Agent"""
    
    def setUp(self):
        self.scout = OpportunitiesScout()
        self.user = UserProfile(
            user_id="test_user",
            name="Test Artist",
            bio="Test bio about art",
            specialization="Digital art",
            achievements=["Exhibition 1", "Residency"],
            interests=["AI", "creativity"],
            acceptance_rate=0.3
        )
    
    def test_find_opportunities(self):
        """Test finding opportunities"""
        opportunities = self.scout.find_opportunities(self.user, num_candidates=3)
        self.assertGreater(len(opportunities), 0)
        self.assertLessEqual(len(opportunities), 3)
    
    def test_relevance_score_calculation(self):
        """Test relevance score is between 0 and 1"""
        opp = self.scout.opportunities_db[0]
        score = self.scout._calculate_relevance_score(self.user, opp)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_get_opportunity_by_id(self):
        """Test retrieving opportunity by ID"""
        opp_id = self.scout.opportunities_db[0].id
        opp = self.scout.get_opportunity_by_id(opp_id)
        self.assertIsNotNone(opp)
        self.assertEqual(opp.id, opp_id)


if __name__ == "__main__":
    unittest.main()
