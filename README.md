# CuratAI - Agentic AI for Cultural Visibility & Resilience

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **CuratAI** empowers artists and cultural strategists to achieve professional resolutions—securing speaking opportunities, exhibitions, and grants—through autonomous agentic AI orchestrated by Opik and secured by Web3.

## 🎯 The Problem

Artists spend **40+ hours monthly** on opportunity research, proposal writing, and deadline management. Current systems are:

- **Fragmented**: Opportunities scattered across dozens of platforms
- **Inefficient**: Manual proposal writing without learning loops
- **Inequitable**: Underrepresented artists lack discovery channels
- **Opaque**: No feedback on rejection reasons

## ✨ The Solution

CuratAI deploys **four autonomous agents**:

1. **Opportunity Scout** 🔍 - Finds relevant opportunities from 20+ sources
2. **Proposal Drafter** ✍️ - Generates tailored proposals in user's voice
3. **Adaptive Strategy** 📊 - Learns from outcomes and refines approach
4. **Calendar Manager** 📅 - Tracks deadlines and sends reminders

**Web3 Integration**: DIDs for identity, IPFS for provenance  
**Opik Orchestration**: Full transparency of agent reasoning and metrics

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon.git
cd CuratAI---Commit-To-Change-An-AI-Agents-Hackathon
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export OPIK_API_KEY="your_key"
export OPENAI_API_KEY="your_key"

# Run demo
python src/main.py

# Run tests
pytest tests/
```

## 📁 Project Structure

```
src/
├── agents/              # Core autonomous agents
│   ├── opportunity_scout.py
│   ├── proposal_drafter.py
│   ├── adaptive_strategy.py
│   └── calendar_manager.py
├── web3/                # Decentralized components
│   ├── did_manager.py
│   ├── ipfs_provenance.py
│   └── dao_connector.py
├── opik_integration/    # Monitoring & orchestration
│   ├── opik_metrics.py
│   └── opik_config.yaml
├── utils/               # Helpers
│   ├── config.py
│   ├── data_loader.py
│   └── nlp_tools.py
└── main.py             # Entry point

docs/
├── PRD.md              # Product Requirements
├── HackathonPitch.md   # Elevator pitch
├── Roadmap.md          # Development phases
└── OpikIntegration.md  # Integration guide

examples/
├── demo_script.md      # Pitch script
├── sample_proposals/   # Example outputs
└── hackathon_demo.ipynb
```

## 💡 Key Features

- ✅ **Autonomous Agents**: Scout, Draft, Strategize, Schedule
- ✅ **Web3 Provenance**: DID signatures + IPFS version history
- ✅ **Opik Monitoring**: Full observability of agent reasoning
- ✅ **A/B Testing**: Compare proposal tones and strategies
- ✅ **Outcome Learning**: Adapt based on real feedback
- ✅ **Multi-Format**: Speaking, exhibitions, grants, fellowships

## 📊 Success Metrics

- **Scout Recall**: >85% of relevant opportunities
- **Draft Quality**: >7/10 expert evaluation
- **Deadline Adherence**: >98%
- **Acceptance Rate Improvement**: +5% month-over-month
- **User Time Saved**: 40 hrs → 4 hrs/month

## 🧪 Testing

```bash
pytest tests/              # Run all tests
pytest --cov=src tests/    # With coverage
pytest tests/test_agents.py::TestOpportunitiesScout  # Specific test
```

## 📖 Documentation

- **[PRD](docs/PRD.md)** - Complete feature specifications
- **[Pitch](docs/HackathonPitch.md)** - 2-3 min elevator pitch
- **[Opik Guide](docs/OpikIntegration.md)** - Monitoring & orchestration
- **[Roadmap](docs/Roadmap.md)** - Development timeline

## 🎓 Hackathon Alignment

✅ **Real Problem**: Artists miss 90% of opportunities  
✅ **Beyond Reminders**: Truly autonomous and adaptive  
✅ **Intelligence**: Learns from outcomes  
✅ **Web3**: DIDs + IPFS for provenance  
✅ **Best Use of Opik**: Full transparency  

## 🤝 Contributing

Contributions welcome! Fork → branch → PR

## 📜 License

MIT License - see [LICENSE](LICENSE)

## 💬 Contact

- **GitHub**: [daghondi/CuratAI](https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon)
- **Issues**: Use GitHub Issues

---

**Made with ❤️ for creative professionals**
