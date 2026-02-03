"""
Unit tests for utility modules
"""

import unittest
from src.utils import TextProcessor, ProposalAnalyzer, ConfigManager


class TestTextProcessor(unittest.TestCase):
    """Tests for Text Processing utilities"""
    
    def test_tokenize(self):
        """Test text tokenization"""
        text = "Hello world test"
        tokens = TextProcessor.tokenize(text)
        self.assertEqual(len(tokens), 3)
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "AI creativity art digital technology creative"
        keywords = TextProcessor.extract_keywords(text, num_keywords=3)
        self.assertLessEqual(len(keywords), 3)
        self.assertGreater(len(keywords), 0)
    
    def test_calculate_similarity(self):
        """Test text similarity"""
        text1 = "AI and creativity"
        text2 = "AI and art"
        
        similarity = TextProcessor.calculate_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_word_count(self):
        """Test word counting"""
        text = "one two three four five"
        count = TextProcessor.word_count(text)
        self.assertEqual(count, 5)
    
    def test_readability_score(self):
        """Test readability score"""
        text = "The quick brown fox jumps over the lazy dog."
        score = TextProcessor.readability_score(text)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)


class TestProposalAnalyzer(unittest.TestCase):
    """Tests for Proposal Analysis"""
    
    def test_analyze_proposal(self):
        """Test proposal analysis"""
        proposal = """
        Background: I have 5 years of experience.
        Relevance: This aligns with my interests.
        Outcome: Expected results and impact.
        """
        
        analysis = ProposalAnalyzer.analyze_proposal(proposal)
        self.assertIn("word_count", analysis)
        self.assertIn("keywords", analysis)
        self.assertIn("readability_score", analysis)
    
    def test_score_proposal(self):
        """Test proposal scoring"""
        proposal = """
        Background: I have 5 years of experience in digital art.
        Relevance: This opportunity aligns with my creative interests and goals.
        Outcome: Expected results include visibility and potential collaborations.
        """
        
        score = ProposalAnalyzer.score_proposal(proposal)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 10.0)
    
    def test_align_with_opportunity(self):
        """Test alignment scoring"""
        proposal = "AI and creative practice"
        opportunity = "AI in arts and creativity"
        
        alignment = ProposalAnalyzer.align_with_opportunity(proposal, opportunity)
        self.assertGreaterEqual(alignment, 0.0)
        self.assertLessEqual(alignment, 1.0)


class TestConfigManager(unittest.TestCase):
    """Tests for Configuration Management"""
    
    def setUp(self):
        self.config = ConfigManager()
    
    def test_get_default_values(self):
        """Test getting default config values"""
        log_level = self.config.get("log_level")
        self.assertEqual(log_level, "INFO")
    
    def test_get_nested_values(self):
        """Test getting nested config values"""
        workspace = self.config.get("opik.workspace")
        self.assertIsNotNone(workspace)
    
    def test_get_with_default(self):
        """Test getting value with default"""
        value = self.config.get("nonexistent.key", "default")
        self.assertEqual(value, "default")
    
    def test_get_config_dict(self):
        """Test exporting config as dict"""
        config_dict = self.config.get_config_dict()
        self.assertIn("debug", config_dict)
        self.assertIn("llm", config_dict)


if __name__ == "__main__":
    unittest.main()
