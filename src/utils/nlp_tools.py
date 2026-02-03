"""
NLP Tools and Utilities

Text processing, sentiment analysis, and NLP utilities for proposal drafting
and opportunity analysis.
"""

import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class TextProcessor:
    """Basic text processing utilities"""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple tokenization by splitting on whitespace"""
        return text.lower().split()
    
    @staticmethod
    def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
        """Extract top keywords from text (simplified)"""
        words = TextProcessor.tokenize(text)
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could'
        }
        
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        # Count occurrences
        from collections import Counter
        counted = Counter(keywords)
        return [word for word, _ in counted.most_common(num_keywords)]
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts (simplified).
        Returns value between 0 and 1.
        """
        words1 = set(TextProcessor.tokenize(text1))
        words2 = set(TextProcessor.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def summarize(text: str, num_sentences: int = 3) -> str:
        """
        Simple text summarization (extract key sentences).
        In production, would use advanced NLP models.
        """
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_sentences:
            return text
        
        # Simple heuristic: take first and last sentences plus important ones
        selected = [sentences[0]]  # First sentence
        
        # Find important sentences (contain key terms)
        keywords = TextProcessor.extract_keywords(text, 5)
        for sent in sentences[1:-1]:
            if any(kw in sent.lower() for kw in keywords) and len(selected) < num_sentences - 1:
                selected.append(sent)
        
        selected.append(sentences[-1])  # Last sentence
        
        return '. '.join(selected[:num_sentences]) + '.'
    
    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text"""
        return len(TextProcessor.tokenize(text))
    
    @staticmethod
    def readability_score(text: str) -> float:
        """
        Calculate readability score (simplified Flesch-Kincaid).
        Returns score between 0 and 100 (higher = more readable).
        """
        words = TextProcessor.tokenize(text)
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if not words or sentences == 0:
            return 0.0
        
        # Simplified formula
        readability = 206.835 - (1.015 * (len(words) / max(sentences, 1)))
        return max(0, min(100, readability))


class ProposalAnalyzer:
    """Analyze and score proposals"""
    
    @staticmethod
    def analyze_proposal(proposal_content: str) -> Dict:
        """
        Analyze a proposal for quality and alignment.
        
        Returns:
            Dictionary with quality metrics
        """
        word_count = TextProcessor.word_count(proposal_content)
        keywords = TextProcessor.extract_keywords(proposal_content, 5)
        readability = TextProcessor.readability_score(proposal_content)
        
        analysis = {
            "word_count": word_count,
            "keywords": keywords,
            "readability_score": readability,
            "has_structure": all(
                marker in proposal_content.lower()
                for marker in ["background", "relevance", "outcome"]
            ),
            "tone_indicators": {
                "formal": TextProcessor.extract_keywords("academic professional credentials"),
                "engaging": TextProcessor.extract_keywords("passion personal connection"),
                "impact": TextProcessor.extract_keywords("impact outcome community value")
            }
        }
        
        return analysis
    
    @staticmethod
    def score_proposal(proposal_content: str) -> float:
        """
        Score a proposal from 0-10.
        
        Factors:
        - Word count (optimal range 500-2000)
        - Readability
        - Structure presence
        - Keyword richness
        """
        analysis = ProposalAnalyzer.analyze_proposal(proposal_content)
        
        score = 0.0
        
        # Word count factor (0-3 points)
        word_count = analysis["word_count"]
        if 500 <= word_count <= 2000:
            score += 3.0
        elif 300 <= word_count <= 3000:
            score += 1.5
        
        # Readability factor (0-3 points)
        readability = analysis["readability_score"]
        score += min(3.0, readability / 33.3)
        
        # Structure factor (0-2 points)
        if analysis["has_structure"]:
            score += 2.0
        
        # Keyword richness (0-2 points)
        num_keywords = len(analysis["keywords"])
        score += min(2.0, num_keywords / 5.0)
        
        return min(10.0, score)
    
    @staticmethod
    def align_with_opportunity(proposal: str, opportunity_description: str) -> float:
        """
        Calculate alignment between proposal and opportunity.
        Returns value 0-1.
        """
        similarity = TextProcessor.calculate_similarity(proposal, opportunity_description)
        return min(1.0, similarity)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    sample_proposal = """
    BACKGROUND & QUALIFICATIONS
    
    Alex Chen is a visual artist with 5 years of experience in digital art and creative technology.
    Recent achievements include a solo exhibition at MoMA PS1 and a residency at Eyebeam.
    
    RELEVANCE TO OPPORTUNITY
    
    This proposal directly addresses the need for speakers exploring AI in creative practice.
    My work bridges traditional art and computational thinking, making it highly relevant.
    
    EXPECTED OUTCOMES
    
    Attendees will gain insights into how AI can amplify, not replace, human creativity.
    """
    
    print("\n=== Text Analysis ===\n")
    
    # Analyze proposal
    analysis = ProposalAnalyzer.analyze_proposal(sample_proposal)
    print(f"Word Count: {analysis['word_count']}")
    print(f"Top Keywords: {', '.join(analysis['keywords'][:5])}")
    print(f"Readability Score: {analysis['readability_score']:.1f}")
    print(f"Has Structure: {analysis['has_structure']}")
    
    # Score proposal
    score = ProposalAnalyzer.score_proposal(sample_proposal)
    print(f"\nProposal Score: {score:.1f}/10")
    
    # Alignment
    opportunity = "TED-style talk on AI in arts and creative technology"
    alignment = ProposalAnalyzer.align_with_opportunity(sample_proposal, opportunity)
    print(f"Alignment with opportunity: {alignment:.0%}")
