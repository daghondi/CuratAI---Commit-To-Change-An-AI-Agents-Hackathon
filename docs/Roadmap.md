# CuratAI Roadmap

## Phase 1: MVP (Hackathon - Week 1-2)

### Agents
- [x] Opportunity Scout Agent (mock data, scoring logic)
- [x] Proposal Drafter Agent (GPT-4 integration, prompt engineering)
- [x] Adaptive Strategy Agent (basic outcome tracking & analysis)
- [x] Calendar Manager (deadline extraction & reminder logic)

### Infrastructure
- [x] Opik integration (workflow coordination, experiment tracking)
- [x] Web3 layer (DID creation, IPFS storage)
- [x] Data models (user profile, opportunities, proposals)

### Demo & Docs
- [x] Interactive Jupyter notebook demo
- [x] Sample proposals (3 types)
- [x] PRD & architecture documentation
- [x] Quick-start guide

### Testing
- [x] Unit tests for core agent logic
- [x] Integration tests with Opik
- [ ] End-to-end demo validated

---

## Phase 2: Real Data Integration (Post-Hackathon - Weeks 3-4)

### Data Sources
- [ ] Integrate with real opportunity feeds (e.g., OpenCall.ai, GrantWatch)
- [ ] Add RSS feed parsing for art opportunities
- [ ] LinkedIn/Twitter scraping for speaking opportunities
- [ ] Email parsing for direct opportunities

### User Profiles
- [ ] UI for profile creation (achievements, goals, style)
- [ ] Portfolio import (from website, Google Drive)
- [ ] Skill/interest taxonomy

### Proposal Quality
- [ ] Expert validator (using rubric + feedback)
- [ ] Plagiarism detection
- [ ] A/B testing framework with real users

---

## Phase 3: Personalization & Learning (Weeks 5-8)

### Adaptive Strategy
- [ ] Fine-tune LLM on user's writing style
- [ ] Historical success pattern analysis
- [ ] Feedback loop: outcomes → strategy adjustment
- [ ] Multi-armed bandit approach for tone/style optimization

### Web3 Enhancement
- [ ] Smart contracts for DAO governance (optional)
- [ ] Verifiable credentials for user achievements
- [ ] Decentralized proposal marketplace

---

## Phase 4: Scale & Polish (Weeks 9-12)

### Product
- [ ] Web UI (React/Next.js)
- [ ] Mobile app (React Native) for deadline management
- [ ] Integrations: Google Calendar, Outlook, Slack
- [ ] Email notifications & reminders

### Operations
- [ ] Multi-language support
- [ ] Cost optimization (agent calls, storage)
- [ ] Compliance & data privacy (GDPR, etc.)

### Go-to-Market
- [ ] Beta launch with 50-100 artists
- [ ] Feedback cycles & iteration
- [ ] Freemium pricing model
- [ ] Community building (Discord, events)

---

## Future Vision (Post-2026)

### AI Advancement
- [ ] Multimodal agents (handle images, portfolios)
- [ ] Long-term memory (relationship building with curators)
- [ ] Collaborative agents (users work with AI in real-time)

### Web3 & DAO
- [ ] Artist DAO (decentralized governance of opportunity curation)
- [ ] Tokenized reputation (track verified opportunities & outcomes)
- [ ] DAO treasury (reward creators of great proposals)

### Ecosystem
- [ ] API for third-party integrations
- [ ] Plugin marketplace for custom agents
- [ ] Open standard for proposal sharing & feedback

---

## Success Metrics

### Hackathon
- MVP deployed & demo working
- 3+ external judges can interact with system
- Team presents coherent pitch & vision

### Phase 2 (by end of Q1 2026)
- Real data integrated (5+ opportunity sources)
- 10+ early users on beta
- Average proposal generation time < 2 minutes
- Proposal acceptance rate tracked & reported

### Phase 3 (by end of Q2 2026)
- 100+ users
- Measurable improvement in acceptance rates (tracked across cohorts)
- Strategy agent recommendations validated by users
- Web3 provenance demonstrably useful (e.g., in dispute resolution)

### Phase 4 (by end of 2026)
- Paid subscribers: 500+
- Annual recurring revenue (ARR): $50k+
- Active DAO with 20+ governance votes
- Open-source community contributions (forks, PRs)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LLM quality inconsistency | Opik experiment tracking, human validation, fine-tuning |
| User data privacy | Local-first architecture, federated learning (future) |
| Opportunity source availability | Multiple sources, fallback to user-curated feeds |
| Agent failure modes | Clear fallbacks to human review, Opik monitoring |
| Market adoption | Early community building, free tier, showcase success stories |

---

## Open Decisions

- [ ] Should agents handle feedback from rejected proposals? (How?)
- [ ] Revenue model: Freemium, SaaS, or community-driven?
- [ ] DAO governance: When to activate? (At 100 users? 1000?)
- [ ] Expansion to other creative fields? (Writers, musicians, etc.)

---

*Last updated: February 2026*
