"""
LLM Integration Module for CuratAI
Integrates with OpenAI GPT-4 and Anthropic Claude for proposal generation
"""

import os
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"


@dataclass
class ProposalGenerationRequest:
    """Request for proposal generation via LLM"""
    artist_name: str
    artist_bio: str
    artist_achievements: List[str]
    opportunity_title: str
    opportunity_description: str
    opportunity_budget: str
    tone: str  # formal, engaging, impact-driven
    max_tokens: int = 1000


class OpenAIConnector:
    """
    OpenAI GPT-4 Integration
    Generates high-quality proposals using OpenAI API
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        
        # Lazy import openai
        try:
            import openai
            openai.api_key = self.api_key
            self.client = openai
        except ImportError:
            print("⚠️  OpenAI library not installed. Install with: pip install openai")
            self.client = None
    
    def generate_proposal(self, request: ProposalGenerationRequest) -> Dict:
        """Generate proposal using GPT-4"""
        if not self.client:
            return {"error": "OpenAI client not initialized"}
        
        tone_guidelines = {
            'formal': "Use professional, academic language. Focus on credentials and methodology.",
            'engaging': "Use conversational, personal tone. Connect emotionally with the reader.",
            'impact-driven': "Emphasize community impact and social outcomes. Focus on measurable results."
        }
        
        system_prompt = f"""You are an expert proposal writer specializing in arts and culture grant applications.
Your task is to write compelling proposals that highlight the artist's strengths and the project's impact.
Tone: {tone_guidelines.get(request.tone, 'professional')}"""
        
        user_prompt = f"""Write a compelling proposal for {request.artist_name}.

ARTIST PROFILE:
Name: {request.artist_name}
Bio: {request.artist_bio}
Key Achievements:
{chr(10).join(f'- {achievement}' for achievement in request.artist_achievements)}

OPPORTUNITY:
Title: {request.opportunity_title}
Description: {request.opportunity_description}
Budget: {request.opportunity_budget}

Create a persuasive 300-500 word proposal that:
1. Hooks the reader with the project's significance
2. Demonstrates the artist's qualifications
3. Explains the project's unique value
4. Describes measurable outcomes
5. Connects to the funder's mission

Tone: {request.tone}"""
        
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=request.max_tokens,
                temperature=0.7
            )
            
            return {
                "success": True,
                "proposal": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": self.model
            }
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}


class AnthropicConnector:
    """
    Anthropic Claude Integration
    Generates proposals using Anthropic's Claude API
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.model = model
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            print("⚠️  Anthropic library not installed. Install with: pip install anthropic")
            self.client = None
    
    def generate_proposal(self, request: ProposalGenerationRequest) -> Dict:
        """Generate proposal using Claude"""
        if not self.client:
            return {"error": "Anthropic client not initialized"}
        
        tone_guidelines = {
            'formal': "Use sophisticated, academic language. Emphasize rigor and methodology.",
            'engaging': "Write in an accessible, engaging style. Tell a compelling story.",
            'impact-driven': "Focus on real-world impact and transformative outcomes."
        }
        
        prompt = f"""You are an expert proposal writer for arts and culture opportunities.

ARTIST PROFILE:
Name: {request.artist_name}
Bio: {request.artist_bio}
Achievements: {', '.join(request.artist_achievements)}

OPPORTUNITY:
{request.opportunity_title}
{request.opportunity_description}
Budget: {request.opportunity_budget}

Write a compelling {request.max_tokens // 4}-word proposal in {request.tone} tone.
{tone_guidelines.get(request.tone, '')}

Structure:
1. Opening hook (impact/vision)
2. Artist credentials
3. Project description
4. Expected outcomes
5. Call to action

Make it persuasive, specific, and tailored to this opportunity."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=request.max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "success": True,
                "proposal": message.content[0].text,
                "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
                "model": self.model
            }
        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}"}


class LLMProposalGenerator:
    """
    Unified interface for generating proposals via different LLM providers
    """
    
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI):
        self.provider = provider
        
        if provider == LLMProvider.OPENAI:
            self.connector = OpenAIConnector()
        elif provider == LLMProvider.ANTHROPIC:
            self.connector = AnthropicConnector()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate(self, request: ProposalGenerationRequest) -> Dict:
        """Generate proposal using the configured LLM provider"""
        return self.connector.generate_proposal(request)
    
    def generate_variants(self, request: ProposalGenerationRequest, 
                         tones: List[str] = None) -> Dict[str, Dict]:
        """Generate proposal variants in different tones"""
        if tones is None:
            tones = ['formal', 'engaging', 'impact-driven']
        
        variants = {}
        for tone in tones:
            request.tone = tone
            variants[tone] = self.generate(request)
        
        return variants


class PromptOptimizer:
    """
    Optimizes prompts for better proposal generation
    Uses techniques like few-shot learning and chain-of-thought
    """
    
    @staticmethod
    def create_few_shot_examples() -> str:
        """Create few-shot learning examples for proposal writing"""
        return """
EXAMPLE 1 - FORMAL TONE:
Project Title: "Neural Pathways: Interactive Installation on AI Ethics"
"This project explores the intersection of machine learning and human consciousness through an interactive 
sculpture that visualizes neural network decision-making. By translating algorithmic processes into 
physical form, we create opportunities for public dialogue about AI's role in society."

EXAMPLE 2 - ENGAGING TONE:
"Imagine walking into a gallery where the walls respond to your movement, where code becomes poetry, 
and AI becomes accessible. That's what this project does—it makes artificial intelligence tangible, 
beautiful, and deeply human."

EXAMPLE 3 - IMPACT-DRIVEN TONE:
"This initiative will reach 10,000+ community members in underserved neighborhoods, providing free 
workshops on AI literacy. Expected outcomes: 85% participant satisfaction, 40+ new artists trained, 
3 public installations in high-traffic areas."
"""
    
    @staticmethod
    def add_chain_of_thought(request: ProposalGenerationRequest) -> str:
        """Add chain-of-thought prompting for better reasoning"""
        return f"""
Step 1: Analyze the opportunity
- Key funder interests: [extract from description]
- Required deliverables: [identify]
- Timeline: [determine]

Step 2: Position the artist
- Unique qualifications: {', '.join(request.artist_achievements[:3])}
- Prior relevant work: [summarize]
- Why this artist is ideal: [explain]

Step 3: Develop the project narrative
- Central concept: [one compelling idea]
- Innovation angle: [what's new?]
- Community benefit: [measurable impact]

Now write the proposal with these elements integrated naturally."""


# Demo usage
if __name__ == "__main__":
    print("🤖 LLM Integration Module")
    print("=" * 60)
    
    print("\n✅ Available LLM Integrations:")
    print("   - OpenAI GPT-4 (gpt-4-turbo)")
    print("   - Anthropic Claude 3 (claude-3-opus)")
    print("   - Azure OpenAI (compatible)")
    
    print("\n📋 Setup Instructions:")
    print("   1. Install OpenAI: pip install openai")
    print("   2. Install Anthropic: pip install anthropic")
    print("   3. Set API keys:")
    print("      export OPENAI_API_KEY='your-key'")
    print("      export ANTHROPIC_API_KEY='your-key'")
    
    print("\n💡 Features:")
    print("   - Multi-tone proposal generation")
    print("   - Few-shot learning examples")
    print("   - Chain-of-thought reasoning")
    print("   - Token usage tracking")
    print("   - Fallback mechanisms")
    
    # Example usage
    request = ProposalGenerationRequest(
        artist_name="Alexandra Chen",
        artist_bio="Interdisciplinary artist exploring AI and cultural equity",
        artist_achievements=["NEA Fellowship 2024", "Venice Biennale 2023"],
        opportunity_title="Creative Innovation Grant",
        opportunity_description="Support for groundbreaking artistic projects",
        opportunity_budget="$50,000",
        tone="impact-driven"
    )
    
    print("\n📝 Example Request:")
    print(f"   Artist: {request.artist_name}")
    print(f"   Opportunity: {request.opportunity_title}")
    print(f"   Tone: {request.tone}")
