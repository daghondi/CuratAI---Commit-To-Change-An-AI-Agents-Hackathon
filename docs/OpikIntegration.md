# CuratAI Opik Integration Guide

## Overview

**Opik** is the orchestration and observability backbone of CuratAI. It provides:

1. **Workflow Orchestration**: Coordinate multi-agent tasks with clear handoffs
2. **Experiment Tracking**: Compare different proposal strategies systematically
3. **Metrics & Monitoring**: Track agent performance, LLM costs, success rates
4. **Dashboard**: Real-time visibility into agent behavior and outcomes

---

## Architecture: How Opik Fits In

```
┌──────────────────────────────────────────────────────────────┐
│                    CuratAI Application                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  User Profile → [Opportunity Scout] → Opportunities          │
│                       ↓                                       │
│                  [Opik Logging]                              │
│                       ↓                                       │
│  Opportunity → [Proposal Drafter] → Draft Proposal           │
│                       ↓                                       │
│                  [Opik Experiment]                           │
│                       ↓                                       │
│  Proposal → [Human Review] → Final Proposal                  │
│                       ↓                                       │
│              [Outcome Recorded]                              │
│                       ↓                                       │
│  Outcome → [Adaptive Strategy] → Recommendations             │
│                       ↓                                       │
│                  [Opik Dashboard]                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Core Opik Integrations

### 1. Workflow Orchestration

**Purpose**: Track multi-step processes and agent handoffs

**Implementation**:
```python
from opik import track

@track(name="opportunity_selection_workflow")
def run_workflow(user_profile):
    # Step 1: Scout Agent finds opportunities
    opportunities = scout_agent.find_opportunities(user_profile)
    
    # Step 2: Draft Agent creates proposals
    proposals = []
    for opp in opportunities:
        draft = drafter_agent.generate_proposal(user_profile, opp)
        proposals.append(draft)
    
    # Step 3: Strategy Agent provides feedback
    strategies = adaptive_agent.analyze(proposals)
    
    return proposals, strategies
```

**Opik Captures**:
- Function call & parameters
- Execution time
- Sub-agent calls
- LLM calls (tokens, cost)
- Errors & exceptions

---

### 2. Experiment Tracking

**Purpose**: Compare different proposal strategies (A/B testing)

**Experiments in CuratAI**:

#### Experiment 1: Tone Comparison
Compare 3 proposal tones for the same opportunity:
- **Formal**: Academic, professional language
- **Engaging**: Conversational, personal touch
- **Impact-Driven**: Focus on outcomes & community benefit

**Evaluation Metrics**:
- User preference (subjective)
- Readability score (objective)
- LLM quality assessment

#### Experiment 2: Strategy Adaptation
Test two hypothesis:
- **A**: Always emphasize past achievements first
- **B**: Always emphasize relevance to opportunity first

**Evaluation**:
- Success rate (acceptance rate)
- User time-to-review
- Feedback quality

**Implementation**:
```python
from opik.opik_names import OpikNames
from opik import evaluate

# Define variants
variants = {
    "formal": "Use academic, professional language",
    "engaging": "Use conversational, personal tone",
    "impact": "Focus on outcomes and community benefit"
}

# Run experiment
results = evaluate(
    dataset="opportunities_2026_feb",
    scoring_fn=score_proposal_quality,
    model_fn=generate_proposal_variant,
    variants=variants,
)
```

---

### 3. Metrics & Monitoring

**Key Metrics**:

| Metric | Definition | Target |
|--------|-----------|--------|
| `scout_recall` | % of relevant opportunities found | > 85% |
| `draft_quality` | Expert score of generated proposal | > 7/10 |
| `user_review_time` | Minutes to review & edit proposal | < 10 min |
| `acceptance_rate` | Submissions accepted / total submitted | > 30% |
| `strategy_improvement` | Improvement in acceptance rate over time | +5% per month |
| `token_cost` | Avg tokens per proposal generation | < 2000 |

**Implementation**:
```python
from opik import get_client

client = get_client()

# Log custom metric after submission outcome
client.log_metric(
    experiment_id="exp_001",
    metric_name="acceptance_rate",
    value=0.35,
    metadata={"proposal_type": "grant", "tone": "impact"}
)
```

---

### 4. Dashboard & Visualization

**Dashboard URL**: (Configured in `opik_config.yaml`)

**Dashboard Sections**:

#### Section A: Agent Workflows
- Timeline of agent calls
- Success/failure rates per agent
- Average execution time per task

#### Section B: Experiments
- Comparison of proposal tones
- Strategy adaptation results
- User preference voting

#### Section C: Metrics
- Acceptance rate trends
- Cost per proposal
- User engagement metrics

#### Section D: Logs
- Individual agent runs
- LLM prompt/response pairs
- Error traces

---

## Configuration: `opik_config.yaml`

```yaml
opik:
  # Opik API configuration
  api_key: "${OPIK_API_KEY}"  # Set via environment variable
  workspace: "curatai-production"
  project_name: "curataI-core"
  
  # Logging settings
  logging:
    level: "INFO"
    log_llm_calls: true
    log_agent_calls: true
    
  # Experiment tracking
  experiments:
    enabled: true
    auto_log_metrics: true
    
  # Dashboard
  dashboard:
    enabled: true
    public_url: "https://opik.comet.ml/curatai"
    
  # Cost tracking
  cost_tracking:
    enabled: true
    alert_threshold: 100  # Alert if daily cost exceeds $100
    
  # Retention
  retention_days: 90
```

---

## Integration Points in Code

### 1. Opportunity Scout Agent
```python
# File: src/agents/opportunity_scout.py

from opik import track

@track(name="scout_agent_find_opportunities")
def find_opportunities(user_profile, num_candidates=10):
    """Find top opportunities for user profile"""
    # ... implementation
    return opportunities
```

### 2. Proposal Drafter Agent
```python
# File: src/agents/proposal_drafter.py

from opik import track, evaluate

@track(name="drafter_agent_generate_proposal")
def generate_proposal(user_profile, opportunity, tone="balanced"):
    """Generate proposal draft with specified tone"""
    # ... implementation
    return proposal_draft

@evaluate(metric_fn=assess_proposal_quality)
def generate_proposal_with_evaluation(user_profile, opportunity):
    """Generate and immediately evaluate proposal"""
    # ... implementation
```

### 3. Adaptive Strategy Agent
```python
# File: src/agents/adaptive_strategy.py

from opik import track

@track(name="strategy_agent_analyze_outcomes")
def analyze_outcomes(submission_history):
    """Analyze patterns in past submissions"""
    # ... implementation
    return recommendations
```

### 4. Main Orchestration
```python
# File: src/main.py

from opik import track, get_client

@track(name="curataI_main_workflow")
def run_curataI(user_profile):
    """Main CuratAI workflow orchestration"""
    
    # Log workflow start
    client = get_client()
    run_id = client.start_run(name="full_workflow")
    
    # Step 1: Find opportunities
    opportunities = find_opportunities(user_profile)
    
    # Step 2: Generate proposals
    proposals = []
    for opp in opportunities:
        proposal = generate_proposal(user_profile, opp)
        proposals.append(proposal)
    
    # Step 3: Analyze strategy
    recommendations = analyze_outcomes(client.get_history())
    
    # Log completion
    client.log_metric("workflow_completed", 1)
    
    return proposals, recommendations
```

---

## Experiment Results Examples

### Tone Comparison (Sample Results)
```json
{
  "experiment_id": "tone_comparison_001",
  "timestamp": "2026-02-10T10:00:00Z",
  "results": {
    "formal": {
      "avg_quality_score": 7.2,
      "user_preference_votes": 12,
      "user_review_time_sec": 180
    },
    "engaging": {
      "avg_quality_score": 7.8,
      "user_preference_votes": 28,
      "user_review_time_sec": 150
    },
    "impact": {
      "avg_quality_score": 7.5,
      "user_preference_votes": 20,
      "user_review_time_sec": 160
    }
  },
  "winner": "engaging"
}
```

### Strategy Adaptation (Sample Results)
```json
{
  "experiment_id": "strategy_adaptation_001",
  "hypothesis": "Impact-first strategy vs. Achievement-first",
  "duration_days": 30,
  "results": {
    "achievement_first": {
      "acceptance_rate": 0.28,
      "proposals_submitted": 15,
      "accepted": 4
    },
    "impact_first": {
      "acceptance_rate": 0.35,
      "proposals_submitted": 14,
      "accepted": 5
    }
  },
  "winner": "impact_first",
  "improvement": "+7 percentage points"
}
```

---

## Running Opik Locally (Development)

```bash
# 1. Start Opik Docker container
docker run -d -p 5173:5173 comet/opik:latest

# 2. Configure API endpoint
export OPIK_API_ENDPOINT="http://localhost:5173"

# 3. Run CuratAI with Opik logging
python src/main.py

# 4. View dashboard at http://localhost:5173
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `API_KEY not set` | Export `OPIK_API_KEY` environment variable |
| `Connection refused` | Check Opik server is running (Docker) |
| `Metrics not appearing` | Ensure `log_llm_calls: true` in config |
| `High costs` | Check experiment count, consider sampling |

---

## Next Steps

1. **Implement**: Integrate `@track` decorator in all agents
2. **Configure**: Set `opik_config.yaml` with API keys
3. **Test**: Run demo locally with Opik dashboard
4. **Monitor**: Track metrics during hackathon presentation
5. **Iterate**: Use experiment results to improve agent prompts

---

*For more Opik documentation, see: https://opik.comet.ml/docs*
