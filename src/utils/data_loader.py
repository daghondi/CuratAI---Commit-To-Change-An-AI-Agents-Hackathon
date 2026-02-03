"""
Utility functions for data loading and NLP

Provides helper functions for loading data, processing text, and general utilities
"""

import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and manages application data"""
    
    @staticmethod
    def load_opportunities_from_json(file_path: str) -> List[Dict]:
        """Load opportunities from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} opportunities from {file_path}")
            return data
        except FileNotFoundError:
            logger.warning(f"Opportunities file not found: {file_path}")
            return []
    
    @staticmethod
    def load_user_profile_from_json(file_path: str) -> Optional[Dict]:
        """Load user profile from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded user profile from {file_path}")
            return data
        except FileNotFoundError:
            logger.warning(f"User profile file not found: {file_path}")
            return None
    
    @staticmethod
    def save_data_to_json(data: any, file_path: str):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")


class NLPTools:
    """Natural Language Processing utilities"""
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate simple text similarity (word overlap)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
        """Extract top keywords from text"""
        words = text.lower().split()
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were'}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Return unique keywords
        return list(set(keywords))[:num_keywords]
    
    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """Calculate simple readability score (0.0 to 1.0)"""
        if not text:
            return 0.0
        
        # Simple metrics
        sentences = text.split('.')
        words = text.split()
        
        if not sentences or not words:
            return 0.0
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        
        # Score based on average words per sentence
        # Ideal is 15-20 words per sentence
        if avg_words_per_sentence < 10:
            score = 0.7
        elif avg_words_per_sentence < 15:
            score = 0.9
        elif avg_words_per_sentence < 20:
            score = 1.0
        elif avg_words_per_sentence < 25:
            score = 0.8
        else:
            score = 0.6
        
        return min(1.0, score)


class Config:
    """Configuration management"""
    
    DEFAULT_CONFIG = {
        "app_name": "CuratAI",
        "version": "0.1.0",
        "environment": "development",
        "log_level": "INFO",
        "max_proposals_per_opportunity": 3,
        "reminder_days_before_deadline": 7,
    }
    
    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict:
        """Load configuration from file or use defaults"""
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded config from {config_path}")
                return {**Config.DEFAULT_CONFIG, **config}
            except Exception as e:
                logger.warning(f"Error loading config: {e}. Using defaults.")
        
        return Config.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def get_config_value(key: str, default: any = None) -> any:
        """Get a specific config value"""
        config = Config.load_config()
        return config.get(key, default)


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    # Test NLP tools
    print("\n=== NLP Tools Demo ===\n")
    
    text1 = "CuratAI helps artists find opportunities for speaking engagements and exhibitions"
    text2 = "CuratAI is a platform that connects artists with speaking opportunities and exhibitions"
    
    similarity = NLPTools.calculate_similarity(text1, text2)
    print(f"Similarity score: {similarity:.2%}")
    
    keywords = NLPTools.extract_keywords(text1)
    print(f"Keywords: {keywords}")
    
    readability = NLPTools.calculate_readability_score(text1)
    print(f"Readability score: {readability:.2%}")
    
    # Test Config
    print("\n=== Config Demo ===\n")
    config = Config.load_config()
    print(f"App name: {config['app_name']}")
    print(f"Version: {config['version']}")
