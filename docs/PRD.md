# CuratAI - Product Requirements Document

## Executive Summary

**CuratAI** is an agentic AI system designed to empower artists, cultural strategists, and creative professionals to achieve their professional resolutions by autonomously identifying, drafting, and managing submissions for high-impact opportunities—including speaking engagements, exhibitions, and grant applications.

By leveraging multi-agent orchestration with **Opik**, Web3 provenance tracking, and adaptive reasoning, CuratAI demonstrates what true agentic AI looks like: autonomous action, intelligent adaptation, and persistent goal achievement.

---

## Problem Statement

Creative professionals face significant barriers to scaling their career opportunities:

1. **Opportunity Discovery**: Manually scouring websites, newsletters, and networks for suitable opportunities is time-consuming and inefficient.
2. **Proposal Quality**: Tailoring proposals to specific opportunity requirements and audience preferences requires deep contextual understanding.
3. **Portfolio Management**: Tracking submissions, responses, and outcomes across multiple platforms lacks centralization.
4. **Adaptive Strategy**: Without feedback loops, professionals cannot learn and adjust their approach based on success rates.
5. **Credibility & Provenance**: In a world of AI-generated content, proving authorship and the creative intent behind proposals is increasingly important.

---

## Proposed Solution

### Core Value Proposition

CuratAI combines four key capabilities:

#### 1. **Opportunity Scout Agent**
- Scans multiple opportunity sources (APIs, RSS feeds, databases)
- Ranks opportunities by relevance to the user's profile
- Alerts users to high-fit opportunities in real-time
- Learns user preferences over time

#### 2. **Proposal Drafter Agent**
- Automatically generates initial drafts for applications, CVs, artist statements
- Incorporates user's unique voice, achievements, and vision
- Tailors content to opportunity-specific requirements and judging criteria
- Supports multiple formats: grant applications, exhibition proposals, speaking abstracts

#### 3. **Adaptive Strategy Agent**
- Tracks outcomes of past submissions (accepted/rejected/pending)
- Analyzes patterns to optimize future proposal strategy
- A/B tests different tones, framing, and emphasis areas
- Provides data-driven recommendations for improvement

#### 4. **Calendar & Deadline Manager**
- Centralizes submission deadlines and follow-up schedules
- Sends proactive reminders
- Integrates with user calendars (Google Calendar, Outlook)
- Tracks timeline for multi-stage opportunities

### Secondary: Web3 & Provenance Layer

- **DID (Decentralized Identity)**: Cryptographically prove author identity and version history
- **IPFS Provenance**: Store immutable records of proposal versions and feedback
- **DAO Governance** (Future): Community voting on opportunity recommendations and validation

### Orchestration: Opik Integration

- **Agent Orchestration**: Coordinate multi-agent workflows with clear handoffs
- **Experiment Tracking**: Compare different proposal strategies (tone, structure, emphasis)
- **Observability Dashboard**: Monitor agent performance, success rates, and cost
- **Feedback Integration**: Use real-world outcomes to refine agent behavior

---

## Core Features & User Flows

### Feature 1: Opportunity Discovery
**Actor**: Opportunity Scout Agent  
**Trigger**: User sets profile (goals, achievements, interests)  
**Flow**:
1. Agent monitors opportunity feeds
2. Scores each opportunity against user profile
3. Presents top candidates with relevance explanation
4. User can accept, reject, or request more context

**Success Metric**: High relevance of suggested opportunities (measured by user engagement)

---

### Feature 2: Proposal Generation
**Actor**: Proposal Drafter Agent  
**Trigger**: User selects an opportunity  
**Flow**:
1. Agent analyzes opportunity requirements
2. Retrieves user's profile, past work, and achievements
3. Generates draft proposal with multiple tone/emphasis variants
4. User reviews, edits, and approves before submission
5. Agent stores version history on IPFS

**Success Metric**: Time saved vs. manual drafting; quality of generated content

---

### Feature 3: Strategy Adaptation
**Actor**: Adaptive Strategy Agent  
**Trigger**: Submission outcomes are logged (accepted/rejected)  
**Flow**:
1. Agent analyzes patterns across submissions
2. Identifies successful vs. unsuccessful traits
3. Recommends adjustments for future proposals
4. Runs experiments via Opik to test hypotheses

**Success Metric**: Improvement in acceptance rate over time

---

### Feature 4: Calendar & Deadline Management
**Actor**: Calendar Manager  
**Trigger**: Submissions logged or opportunities accepted  
**Flow**:
1. Agent extracts deadlines and next steps
2. Sets reminders (email, calendar invite)
3. Tracks status of multi-stage processes
4. Sends follow-up prompts if no action taken

**Success Metric**: Zero missed deadlines; proactive user engagement

---

## Technical Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                        CuratAI System                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Opportunity │  │  Proposal    │  │   Adaptive  │     │
│  │    Scout     │  │   Drafter    │  │  Strategy   │     │
│  │    Agent     │  │    Agent     │  │   Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Opik Orchestration & Monitoring              │  │
│  │  - Workflow coordination                             │  │
│  │  - Experiment tracking                               │  │
│  │  - Performance metrics & dashboards                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Web3 &   │  │   Data     │  │   NLP &    │           │
│  │ Provenance │  │   Layer    │  │   Utils    │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Dependencies

- **LLM**: OpenAI GPT-4, Anthropic Claude (for proposal generation & analysis)
- **Orchestration**: Opik (workflow + monitoring)
- **Web3**: 
  - DID: `did-key` or similar
  - IPFS: Pinata or similar service
  - Blockchain: Optional (for future DAO features)
- **Data**: SQLite/PostgreSQL for local/cloud state
- **APIs**: OpenAI, external opportunity feeds, calendar services

---

## Success Criteria

### MVP (Hackathon Phase)
- [ ] Opportunity Scout identifies 5+ relevant opportunities from test dataset
- [ ] Proposal Drafter generates usable draft proposals
- [ ] Adaptive Strategy tracks and reports on past submission outcomes
- [ ] Opik dashboard visualizes agent workflows and metrics
- [ ] Web3 provenance: Store version history on IPFS
- [ ] Working demo with sample user profile and opportunities

### Post-MVP
- [ ] Real-time integration with major opportunity databases
- [ ] Multi-language support for international opportunities
- [ ] Mobile app for deadline reminders
- [ ] Community validation via DAO governance
- [ ] Integration with major calendar systems

---

## User Experience Flow

```
1. User Creates Profile
   ↓
2. System Monitors Opportunities
   ↓
3. High-Fit Opportunities Presented
   ↓
4. User Selects Opportunity
   ↓
5. Proposal Draft Generated (with variants)
   ↓
6. User Reviews & Edits
   ↓
7. Version Stored on IPFS, DID Created
   ↓
8. Proposal Submitted
   ↓
9. Outcome Tracked
   ↓
10. Strategy Refined Based on Data
```

---

## Hackathon Context: "Commit to Change"

CuratAI embodies the hackathon's theme by:

1. **Agentic AI in Action**: Not just a tool, but autonomous agents that reason, act, and adapt
2. **Empowering Creatives**: Removes barriers to opportunity discovery and submission
3. **Decentralized Trust**: Web3 provenance ensures AI-generated content can be verified and attributed
4. **Community Benefit**: Artists and cultural professionals can reach more opportunities
5. **Responsible AI**: Opik provides transparency into agent decision-making and performance

---

## Demo & Deliverables

### For Hackathon Submission
1. **Working Demo**: Interactive notebook showing all four agents in action
2. **Sample Proposals**: 3 proposals (speaking, exhibition, grant) with variants
3. **Opik Dashboard**: Showing experiment results and agent performance
4. **Pitch Deck**: 2–3 minute video or slides

### Documentation
- This PRD
- Architecture diagram
- Quick-start guide
- Opik integration documentation

---

## Open Questions & Future Scope

1. How should agents handle rejection feedback? (e.g., explicit feedback vs. pattern inference)
2. Should users be able to provide explicit strategy constraints? (e.g., "always emphasize diversity impact")
3. How to validate proposal quality before submission? (human review, expert scoring, etc.)
4. DAO governance: When/how should community voting be triggered?
5. Sustainability: Revenue model for post-hackathon growth (freemium, enterprise licensing)?

---

## Conclusion

CuratAI transforms creative career management from a manual, time-consuming process into an intelligent, data-driven system. By demonstrating true agentic AI—with autonomous reasoning, multi-step planning, and continuous adaptation—CuratAI shows how AI can empower, not replace, human creativity.
