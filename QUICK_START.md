# 🚀 CuratAI Quick Start Guide

**Get CuratAI running in 5 minutes**

---

## 📋 Prerequisites

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/)
- **PostgreSQL** (optional) - For persistent data
- **Docker** (optional) - For containerized deployment

---

## ⚡ Option 1: Quick Start (5 minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon.git
cd CuratAI---Commit-To-Change-An-AI-Agents-Hackathon
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Demo
```bash
python src/main.py
```

✅ You should see the complete CuratAI workflow in action!

---

## 🐳 Option 2: Docker (3 minutes)

### Step 1: Install Docker
- [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### Step 2: Clone Repository
```bash
git clone https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon.git
cd CuratAI---Commit-To-Change-An-AI-Agents-Hackathon
```

### Step 3: Start Services
```bash
docker-compose up -d
```

### Step 4: Access Applications
- **Backend**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **pgAdmin**: http://localhost:5050
- **Prometheus**: http://localhost:9090 (with `--profile monitoring`)

### View Logs
```bash
docker-compose logs -f backend
```

### Stop Services
```bash
docker-compose down
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
# View coverage report: open htmlcov/index.html
```

### Run Specific Test
```bash
pytest tests/test_agents.py::TestOpportunitiesScout::test_find_opportunities
```

---

## 📓 Interactive Jupyter Demo

```bash
jupyter notebook examples/hackathon_demo.ipynb
```

Explore the system with 9 interactive cells showing:
- User profile creation
- Opportunity scouting
- Proposal generation
- Web3 integration
- Opik orchestration
- Adaptive strategy learning

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
OPIK_API_KEY=your-opik-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/curataai

# Optional APIs
OPENCALL_API_KEY=...
GRANTWATCH_API_KEY=...
SUBMITTABLE_API_KEY=...

# Opik
OPIK_WORKSPACE_NAME=default
```

### Load Configuration
```python
from utils.config import ConfigManager

config = ConfigManager()
api_key = config.get('OPENAI_API_KEY')
```

---

## 📚 Project Structure

```
src/
├── agents/           # 4 autonomous agents
│   ├── opportunity_scout.py
│   ├── proposal_drafter.py
│   ├── adaptive_strategy.py
│   └── calendar_manager.py
├── web3/            # Web3 integration
│   ├── did_manager.py
│   ├── ipfs_provenance.py
│   └── dao_enhanced.py
├── integrations/    # Real APIs
│   ├── real_api_connector.py
│   └── llm_connector.py
├── platform/        # Multi-user platform
│   └── multi_user.py
├── database/        # Database models
│   └── models.py
└── main.py          # Entry point

tests/               # Unit tests (20+ tests)
examples/            # Demo materials
docs/               # Documentation
```

---

## 🎯 Usage Examples

### Example 1: Scout Opportunities
```python
from agents.opportunity_scout import OpportunitiesScout, UserProfile

scout = OpportunitiesScout()
profile = UserProfile(
    name="Alexandra Chen",
    specializations=["digital_art", "installation"],
    interests=["AI ethics", "cultural equity"]
)
opportunities = scout.find_opportunities(profile)

for opp in opportunities:
    print(f"{opp.title} - {opp.relevance_score:.1%}")
```

### Example 2: Generate Proposals
```python
from agents.proposal_drafter import ProposalDrafter

drafter = ProposalDrafter()
proposals = drafter.generate_proposal_variants(profile, opportunity)

for proposal in proposals:
    print(f"Tone: {proposal.tone.value}")
    print(proposal.content)
```

### Example 3: Track with Web3
```python
from web3.did_manager import DIDManager
from web3.ipfs_provenance import IPFSProvenanceManager

did_manager = DIDManager()
did = did_manager.create_did(name="Alexandra Chen")

ipfs = IPFSProvenanceManager()
record = ipfs.store_proposal_version(
    proposal_id="prop_001",
    content=proposal_content,
    artist_did=did['did']
)
print(f"IPFS Hash: {record['ipfs_hash']}")
```

### Example 4: Multi-User Platform
```python
from platform.multi_user import MultiUserPlatform

platform = MultiUserPlatform()
user = platform.create_user(
    email="artist@example.com",
    artist_name="Alexandra Chen"
)

# Track opportunity
platform.track_opportunity(user.user_id, "opp_123", opp_data)

# Get dashboard
dashboard = platform.get_user_dashboard(user.user_id)
print(f"Opportunities tracked: {dashboard['metrics']['opportunities_tracked']}")
```

### Example 5: DAO Governance
```python
from web3.dao_enhanced import EnhancedDAOConnector, BadgeType

dao = EnhancedDAOConnector()
member = dao.register_member_with_tokens("did:example:001", "Alexandra")

# Create recognition proposal
proposal = dao.create_recognition_proposal(
    proposer_did="did:example:001",
    artist_did="did:example:001",
    badge_type=BadgeType.GRANT_WINNER,
    reason="Won NEA Fellowship"
)
```

---

## 📊 Monitoring & Analytics

### View Opik Dashboard
```bash
# Login to Opik workspace
opik login --workspace default

# View metrics
opik metrics list
```

### Database Queries
```python
from database.models import DatabaseRepository

repo = DatabaseRepository("postgresql://...")
users = repo.get_all_users()
submissions = repo.get_submissions_by_status("accepted")
```

### Platform Analytics
```python
from platform.multi_user import PlatformAnalytics

analytics = PlatformAnalytics(platform)
stats = analytics.get_platform_stats()
leaderboard = analytics.get_user_leaderboard('submissions')
```

---

## 🔌 Connecting Real APIs

### OpenCall.ai
```python
from integrations.real_api_connector import OpenCallAIConnector

os.environ['OPENCALL_API_KEY'] = 'your-key'
opencall = OpenCallAIConnector()
opportunities = opencall.search_opportunities({
    'keywords': ['digital art', 'AI'],
    'location': ['US']
})
```

### OpenAI GPT-4
```python
from integrations.llm_connector import LLMProposalGenerator
from integrations.llm_connector import ProposalGenerationRequest

os.environ['OPENAI_API_KEY'] = 'sk-...'
generator = LLMProposalGenerator()

request = ProposalGenerationRequest(
    artist_name="Alexandra Chen",
    opportunity_title="Grant Application",
    tone="impact-driven"
)
result = generator.generate(request)
print(result['proposal'])
```

---

## 📖 Next Steps

1. **Read the PRD** - Full specification in `docs/PRD.md`
2. **Explore Agents** - Check individual agent modules
3. **Run Tests** - Validate everything works
4. **Try Jupyter Demo** - Interactive walkthrough
5. **Connect Real APIs** - Set API keys and test integration
6. **Deploy with Docker** - Run in containers

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in code or use:
docker-compose down
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql --version  # Should be installed
# Or use SQLite (default in dev):
DATABASE_URL=sqlite:///curataai.db
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### API Key Issues
```bash
# Check .env file exists and is readable
cat .env
# Or set directly:
export OPENAI_API_KEY='sk-...'
```

---

## 📞 Support & Community

- **GitHub Issues**: [Report bugs](https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon/issues)
- **Documentation**: [Full docs](https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon/blob/main/docs/PRD.md)
- **Email**: support@curataai.xyz (coming soon)

---

## 📝 License

MIT License - See LICENSE file

---

## 🎉 Ready to Get Started?

```bash
git clone https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon.git
cd CuratAI---Commit-To-Change-An-AI-Agents-Hackathon
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python src/main.py
```

**Enjoy! 🚀**
