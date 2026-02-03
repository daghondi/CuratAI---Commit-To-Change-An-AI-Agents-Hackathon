# CuratAI - AI Agents for Artists and Cultural Strategists

CuratAI empowers artists and cultural strategists to achieve professional goals such as securing speaking opportunities, exhibitions, and grants. It embodies the hackathon's definition of agentic AI by autonomously reasoning, acting, and adapting to obstacles, while leveraging Opik for orchestration, monitoring, and evaluation.

## 🎯 Features

### Agentic AI Capabilities
- **Autonomous Reasoning**: Analyzes goals and develops strategic plans using advanced LLM reasoning
- **Action**: Executes concrete steps toward goal achievement
- **Adaptation**: Dynamically overcomes obstacles with creative solutions

### Goal Types
- **Speaking Opportunities**: Secure conference talks, panel discussions, and workshops
- **Exhibitions**: Obtain gallery shows, museum exhibitions, and art space displays
- **Grants**: Apply for funding from foundations, government agencies, and arts organizations

### Opik Integration
- **Orchestration**: Coordinates multi-step agent workflows
- **Monitoring**: Tracks all agent actions and decisions
- **Evaluation**: Assesses the quality and effectiveness of agent outputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Opik API key (optional, for monitoring)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/daghondi/CuratAI---Commit-To-Change-An-AI-Agents-Hackathon.git
cd CuratAI---Commit-To-Change-An-AI-Agents-Hackathon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running Examples

#### Speaking Opportunity Example
```bash
python -m examples.speaking_opportunity
```
This demonstrates the full agent lifecycle:
- Autonomous reasoning about the goal
- Taking concrete actions
- Adapting to obstacles

#### Exhibition Example
```bash
python -m examples.exhibition
```

#### Grant Example
```bash
python -m examples.grant
```

## 📖 Usage

### Basic Usage

```python
from curatai.models import Goal, GoalType, ArtistProfile
from curatai.agents import CuratAIAgent
import uuid

# Create an artist profile
artist = ArtistProfile(
    name="Your Name",
    discipline="Your Discipline",
    expertise_areas=["Area 1", "Area 2"],
    past_achievements=["Achievement 1", "Achievement 2"]
)

# Initialize the agent
agent = CuratAIAgent(artist)

# Create a goal
goal = Goal(
    goal_id=str(uuid.uuid4()),
    goal_type=GoalType.SPEAKING_OPPORTUNITY,
    title="Secure speaking engagement at major conference",
    description="Get invited to speak about your expertise"
)

# Add goal to agent
agent.add_goal(goal)

# Phase 1: Reasoning
reasoning_result = agent.reason(goal, context="Additional context")
print(reasoning_result["reasoning"])

# Phase 2: Acting
action_result = agent.act(goal, action_plan="Your action plan")
print(f"Progress: {action_result['new_progress']}%")

# Phase 3: Adapting (if obstacles occur)
obstacle = goal.add_obstacle("Description of obstacle")
adaptation_result = agent.adapt(goal, obstacle)
print(adaptation_result["adaptation_strategy"])
```

## 🏗️ Architecture

### Core Components

1. **Models** (`curatai/models/`)
   - `Goal`: Represents professional goals with status tracking
   - `GoalType`: Enumeration of goal types (speaking, exhibition, grant)
   - `ArtistProfile`: Profile information for artists and strategists
   - `Obstacle`: Represents challenges encountered during goal pursuit

2. **Agents** (`curatai/agents/`)
   - `CuratAIAgent`: Main agentic AI with reasoning, action, and adaptation

3. **Utils** (`curatai/utils/`)
   - `OpikTracker`: Integration with Opik for monitoring and evaluation

### Agent Workflow

```
┌─────────────────┐
│  Artist Profile │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Create Goal   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│    REASONING    │─────▶│ Opik Tracking│
│ Analyze & Plan  │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│     ACTING      │─────▶│ Opik Tracking│
│  Execute Steps  │      └──────────────┘
└────────┬────────┘
         │
         ▼
    Obstacle? ──No──▶ Continue
         │
        Yes
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   ADAPTING      │─────▶│ Opik Tracking│
│ Overcome Block  │      └──────────────┘
└────────┬────────┘
         │
         ▼
   Goal Achieved
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPIK_API_KEY`: Your Opik API key (optional, for monitoring)
- `OPIK_WORKSPACE`: Your Opik workspace name (optional)
- `MODEL_NAME`: OpenAI model to use (default: gpt-4)

## 🧪 Testing

Run the example scripts to validate the system:

```bash
# Test all three goal types
python -m examples.speaking_opportunity
python -m examples.exhibition
python -m examples.grant
```

Each example demonstrates:
- ✅ Autonomous reasoning
- ✅ Action execution
- ✅ Obstacle adaptation
- ✅ Opik integration

## 📊 Monitoring with Opik

When configured with Opik credentials, CuratAI automatically tracks:
- All agent reasoning sessions
- Actions taken toward goals
- Adaptation strategies for obstacles
- Performance metrics and evaluations

View your tracked data in the Opik dashboard to:
- Monitor agent performance
- Evaluate decision quality
- Analyze goal achievement patterns
- Optimize agent strategies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

See LICENSE file for details.

## 🎨 Use Cases

### For Artists
- Secure speaking engagements at conferences and events
- Land gallery exhibitions and museum shows
- Obtain funding through grants and fellowships

### For Cultural Strategists
- Position clients for high-profile speaking opportunities
- Connect artists with exhibition venues
- Navigate the grant application landscape

### For Arts Organizations
- Help emerging artists achieve professional milestones
- Track and measure artist development programs
- Optimize support strategies based on data

## 🔮 Future Enhancements

- Additional goal types (residencies, commissions, collaborations)
- Integration with arts opportunity databases
- Multi-agent collaboration for complex goals
- Advanced evaluation metrics
- Real-time deadline tracking and notifications
