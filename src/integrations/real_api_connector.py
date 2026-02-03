"""
Real API Integration Module for CuratAI
Connects to real opportunity data sources and services
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class APIOpportunity:
    """Opportunity from real API"""
    id: str
    title: str
    organization: str
    description: str
    deadline: datetime
    url: str
    type: str  # grant, exhibition, speaking, residency, fellowship
    budget: str
    source: str  # API source (opencall, grantwatch, submittable, etc)
    requirements: List[str] = field(default_factory=list)
    eligibility: Dict = field(default_factory=dict)
    raw_data: Dict = field(default_factory=dict)


class OpenCallAIConnector:
    """
    Connects to OpenCall.ai API for curated opportunities
    https://opencall.ai
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENCALL_API_KEY')
        self.base_url = "https://api.opencall.ai/v1"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def search_opportunities(self, filters: Dict) -> List[APIOpportunity]:
        """
        Search for opportunities with filters
        
        Args:
            filters: {
                'keywords': ['digital art', 'AI'],
                'location': ['US', 'EU'],
                'types': ['exhibition', 'grant', 'speaking'],
                'budget_min': 5000,
                'budget_max': 500000
            }
        """
        try:
            response = self.session.get(
                f"{self.base_url}/opportunities",
                params=filters,
                timeout=10
            )
            response.raise_for_status()
            
            opportunities = []
            for item in response.json().get('results', []):
                opp = APIOpportunity(
                    id=item.get('id'),
                    title=item.get('title'),
                    organization=item.get('organization_name'),
                    description=item.get('description'),
                    deadline=datetime.fromisoformat(item.get('deadline')),
                    url=item.get('url'),
                    type=item.get('opportunity_type', 'general'),
                    budget=item.get('budget', 'Not specified'),
                    source='OpenCall.ai',
                    requirements=item.get('requirements', []),
                    eligibility=item.get('eligibility_criteria', {}),
                    raw_data=item
                )
                opportunities.append(opp)
            
            return opportunities
        except Exception as e:
            print(f"OpenCall.ai error: {e}")
            return []


class GrantWatchConnector:
    """
    Connects to GrantWatch for grant opportunities
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GRANTWATCH_API_KEY')
        self.base_url = "https://api.grantwatch.com/v2"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'X-API-Key': self.api_key})
    
    def search_grants(self, keywords: List[str], filters: Dict) -> List[APIOpportunity]:
        """Search for grants by keywords and filters"""
        try:
            params = {
                'keywords': ' '.join(keywords),
                'entity_type': 'individual',
                **filters
            }
            
            response = self.session.get(
                f"{self.base_url}/grants",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            opportunities = []
            for item in response.json().get('grants', []):
                deadline_str = item.get('deadline')
                deadline = datetime.fromisoformat(deadline_str) if deadline_str else datetime.now() + timedelta(days=30)
                
                opp = APIOpportunity(
                    id=item.get('grant_id'),
                    title=item.get('title'),
                    organization=item.get('sponsor_name'),
                    description=item.get('description'),
                    deadline=deadline,
                    url=item.get('website_url'),
                    type='grant',
                    budget=f"${item.get('max_award', 'Varies')}",
                    source='GrantWatch',
                    eligibility=item.get('eligibility', {}),
                    raw_data=item
                )
                opportunities.append(opp)
            
            return opportunities
        except Exception as e:
            print(f"GrantWatch error: {e}")
            return []


class SubmittableConnector:
    """
    Connects to Submittable API for exhibition calls
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('SUBMITTABLE_API_KEY')
        self.base_url = "https://api.submittable.com/api/v1"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json'
            })
    
    def search_exhibitions(self, keywords: List[str]) -> List[APIOpportunity]:
        """Search for open calls on Submittable"""
        try:
            response = self.session.get(
                f"{self.base_url}/forms",
                params={'search': ' '.join(keywords)},
                timeout=10
            )
            response.raise_for_status()
            
            opportunities = []
            for item in response.json().get('items', []):
                opp = APIOpportunity(
                    id=item.get('id'),
                    title=item.get('name'),
                    organization=item.get('organization'),
                    description=item.get('description'),
                    deadline=datetime.fromisoformat(item.get('close_date')),
                    url=item.get('url'),
                    type='exhibition',
                    budget=item.get('awards', 'Recognition'),
                    source='Submittable',
                    requirements=item.get('submission_requirements', []),
                    raw_data=item
                )
                opportunities.append(opp)
            
            return opportunities
        except Exception as e:
            print(f"Submittable error: {e}")
            return []


class ResidencyConnector:
    """
    Connects to artist residency databases
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('RESIDENCY_API_KEY')
        self.base_url = "https://api.resartis.org/v1"  # ArtistResidencies example
        self.session = requests.Session()
    
    def search_residencies(self, filters: Dict) -> List[APIOpportunity]:
        """Search for residency opportunities"""
        try:
            response = self.session.get(
                f"{self.base_url}/residencies",
                params=filters,
                timeout=10
            )
            response.raise_for_status()
            
            opportunities = []
            for item in response.json().get('results', []):
                opp = APIOpportunity(
                    id=item.get('id'),
                    title=item.get('title'),
                    organization=item.get('institution'),
                    description=item.get('description'),
                    deadline=datetime.fromisoformat(item.get('application_deadline')),
                    url=item.get('apply_url'),
                    type='residency',
                    budget=item.get('stipend', 'Covered'),
                    source='ResArtis',
                    eligibility=item.get('eligibility', {}),
                    raw_data=item
                )
                opportunities.append(opp)
            
            return opportunities
        except Exception as e:
            print(f"ResArtis error: {e}")
            return []


class APIAggregator:
    """
    Aggregates opportunities from multiple real API sources
    """
    
    def __init__(self):
        self.connectors = {
            'opencall': OpenCallAIConnector(),
            'grantwatch': GrantWatchConnector(),
            'submittable': SubmittableConnector(),
            'residencies': ResidencyConnector(),
        }
    
    def search_all(self, keywords: List[str], filters: Dict) -> List[APIOpportunity]:
        """
        Search all connected APIs for opportunities
        
        Args:
            keywords: Artist interests and specializations
            filters: Location, type, budget, etc
        
        Returns:
            Aggregated list of opportunities from all sources
        """
        all_opportunities = []
        
        # Search each connector
        for source, connector in self.connectors.items():
            try:
                if source == 'opencall':
                    opportunities = connector.search_opportunities(filters)
                elif source == 'grantwatch':
                    opportunities = connector.search_grants(keywords, filters)
                elif source == 'submittable':
                    opportunities = connector.search_exhibitions(keywords)
                elif source == 'residencies':
                    opportunities = connector.search_residencies(filters)
                else:
                    continue
                
                all_opportunities.extend(opportunities)
            except Exception as e:
                print(f"Error searching {source}: {e}")
                continue
        
        # Deduplicate by title and organization
        seen = set()
        unique = []
        for opp in all_opportunities:
            key = (opp.title.lower(), opp.organization.lower())
            if key not in seen:
                seen.add(key)
                unique.append(opp)
        
        return unique


# Demo usage
if __name__ == "__main__":
    print("🔗 Real API Integration Module")
    print("=" * 60)
    
    aggregator = APIAggregator()
    
    # Example search
    keywords = ["digital art", "AI ethics", "installation"]
    filters = {
        'location': ['US', 'EU'],
        'types': ['exhibition', 'grant', 'speaking', 'residency'],
        'budget_min': 5000,
    }
    
    print(f"\nSearching for opportunities...")
    print(f"Keywords: {keywords}")
    print(f"Filters: {filters}\n")
    
    # In production, this would return real data
    # For now, demonstrates the structure
    print("✅ API Integration module ready for:")
    print("   - OpenCall.ai (exhibitions, calls)")
    print("   - GrantWatch (grants)")
    print("   - Submittable (open calls)")
    print("   - ResArtis (residencies)")
    print("\nSet API keys via environment variables:")
    print("   OPENCALL_API_KEY")
    print("   GRANTWATCH_API_KEY")
    print("   SUBMITTABLE_API_KEY")
    print("   RESIDENCY_API_KEY")
