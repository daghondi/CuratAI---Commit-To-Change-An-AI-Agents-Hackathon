# CuratAI Architecture

## Overview

CuratAI is an agentic AI system designed to help artists and cultural strategists achieve their professional goals. The system demonstrates autonomous reasoning, action, and adaptation capabilities while leveraging Opik for orchestration, monitoring, and evaluation.

## Core Design Principles

### 1. Agentic AI
The system embodies three core agentic AI capabilities:

- **Autonomous Reasoning**: Uses LLM-powered reasoning to analyze goals and develop strategies
- **Action**: Executes concrete steps toward goal achievement
- **Adaptation**: Dynamically overcomes obstacles with alternative strategies

### 2. Domain-Specific Intelligence
CuratAI is specialized for the arts ecosystem:

- Speaking opportunities (conferences, panels, workshops)
- Exhibition opportunities (galleries, museums, art spaces)
- Grant opportunities (foundations, government agencies, arts organizations)

### 3. Observable and Measurable
Every agent action is tracked and evaluated:

- Opik integration for monitoring
- Progress tracking (0-100%)
- Status management
- Action history

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CuratAI System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              Artist/Strategist Profile                │    │
│  │  - Name, Discipline                                   │    │
│  │  - Expertise Areas                                    │    │
│  │  - Past Achievements                                  │    │
│  └─────────────────────┬─────────────────────────────────┘    │
│                        │                                        │
│                        ▼                                        │
│  ┌───────────────────────────────────────────────────────┐    │
│  │                CuratAIAgent                           │    │
│  │  ┌─────────────────────────────────────────────┐     │    │
│  │  │  Reasoning Engine (LLM-powered)             │     │    │
│  │  │  - Analyzes goals                           │     │    │
│  │  │  - Develops strategies                      │     │    │
│  │  │  - Context-aware planning                   │     │    │
│  │  └─────────────────────────────────────────────┘     │    │
│  │  ┌─────────────────────────────────────────────┐     │    │
│  │  │  Action Executor                            │     │    │
│  │  │  - Generates concrete steps                 │     │    │
│  │  │  - Updates progress                         │     │    │
│  │  │  - Tracks actions taken                     │     │    │
│  │  └─────────────────────────────────────────────┘     │    │
│  │  ┌─────────────────────────────────────────────┐     │    │
│  │  │  Adaptation System                          │     │    │
│  │  │  - Detects obstacles                        │     │    │
│  │  │  - Generates alternatives                   │     │    │
│  │  │  - Resolves blockers                        │     │    │
│  │  └─────────────────────────────────────────────┘     │    │
│  └───────────────────────┬───────────────────────────────┘    │
│                          │                                     │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              Goal Management System                   │    │
│  │  - Speaking Opportunities                             │    │
│  │  - Exhibitions                                        │    │
│  │  - Grants                                             │    │
│  │  - Status: Planning → In Progress → Completed         │    │
│  └─────────────────────┬─────────────────────────────────┘    │
│                        │                                        │
│                        ▼                                        │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              Opik Integration Layer                   │    │
│  │  - Orchestration (workflow coordination)              │    │
│  │  - Monitoring (action tracking)                       │    │
│  │  - Evaluation (quality assessment)                    │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Models (`curatai/models/`)

#### ArtistProfile
- Stores artist/strategist information
- Provides context for AI reasoning
- Includes expertise areas and achievements

#### Goal
- Represents professional objectives
- Tracks status and progress
- Manages obstacles and actions
- Supports three types: Speaking, Exhibition, Grant

#### Obstacle
- Represents challenges encountered
- Tracks resolution status
- Stores resolution strategies

### Agents (`curatai/agents/`)

#### CuratAIAgent
The main agent class implementing agentic AI:

**Methods:**
- `reason(goal, context)`: Analyzes goal and develops strategy
- `act(goal, action_plan)`: Executes actions toward goal
- `adapt(goal, obstacle)`: Generates alternative strategies

**Configuration:**
- `DEFAULT_ACTIONS_PER_STEP`: Number of actions per execution (default: 2)
- `PROGRESS_INCREMENT`: Progress increase per action (default: 20%)

### Utilities (`curatai/utils/`)

#### OpikTracker
Handles all Opik integration:

**Methods:**
- `track_agent_action()`: Logs agent activities
- `start_trace()`: Initiates workflow tracking
- `evaluate_action()`: Assesses action quality

**Features:**
- Graceful degradation when Opik not configured
- Error handling and logging
- Metadata support for detailed tracking

## Data Flow

### 1. Goal Creation Flow
```
User → Create ArtistProfile
     → Create Goal (with type, title, description)
     → Add to Agent
```

### 2. Reasoning Flow
```
Agent.reason() → Build context prompt
              → Call OpenAI API
              → Parse strategic response
              → Track with Opik
              → Return reasoning result
```

### 3. Action Flow
```
Agent.act() → Generate type-specific actions
           → Record actions in goal
           → Update goal status
           → Increment progress
           → Track with Opik
           → Return action result
```

### 4. Adaptation Flow
```
Goal.add_obstacle() → Set status to BLOCKED
                   → Store obstacle details

Agent.adapt() → Analyze obstacle
             → Generate adaptation strategy
             → Resolve obstacle
             → Update goal status
             → Track with Opik
             → Return adaptation result
```

## Goal State Machine

```
┌──────────┐
│ PLANNING │
└────┬─────┘
     │ act()
     ▼
┌──────────────┐     add_obstacle()     ┌─────────┐
│ IN_PROGRESS  │ ────────────────────▶  │ BLOCKED │
└──────┬───────┘                         └────┬────┘
       │                                      │
       │ progress = 100                       │ adapt()
       ▼                                      ▼
┌──────────────┐                         Back to
│  COMPLETED   │                         IN_PROGRESS
└──────────────┘
```

## Integration Points

### OpenAI API
- **Purpose**: Powers reasoning and adaptation
- **Model**: GPT-4 (configurable)
- **Usage**: Strategic analysis, plan generation, obstacle resolution
- **Configuration**: Via `OPENAI_API_KEY` environment variable

### Opik Platform
- **Purpose**: Orchestration, monitoring, evaluation
- **Configuration**: Via `OPIK_API_KEY` and `OPIK_WORKSPACE`
- **Features**: 
  - Action tracking
  - Workflow tracing
  - Performance evaluation
  - Optional (graceful degradation)

## Extensibility

### Adding New Goal Types
1. Add enum value to `GoalType` in `models/__init__.py`
2. Add action generation logic in `CuratAIAgent._generate_actions()`
3. Update system prompt in `CuratAIAgent._get_system_prompt()`
4. Create example in `examples/` directory

### Custom Agent Behaviors
1. Extend `CuratAIAgent` class
2. Override `reason()`, `act()`, or `adapt()` methods
3. Adjust configuration constants
4. Add custom tracking metadata

### Enhanced Evaluation
1. Extend `OpikTracker.evaluate_action()`
2. Add custom metrics
3. Implement scoring algorithms
4. Create evaluation reports

## Performance Characteristics

### Scalability
- Single agent can manage multiple goals
- Each goal tracked independently
- Asynchronous tracking to Opik
- No database dependencies (in-memory state)

### Reliability
- Graceful error handling
- Optional dependencies (Opik)
- Environment-based configuration
- No single points of failure

### Observability
- All actions logged to Opik
- Progress tracking in real-time
- Obstacle history maintained
- Action history preserved

## Security Considerations

### API Key Management
- Environment variable storage
- No hardcoded credentials
- `.env` file not committed to repository
- Example configuration provided

### Data Privacy
- No persistent storage of sensitive data
- Artist profiles in memory only
- No external data sharing (except Opik)
- User controls all data

### Input Validation
- Pydantic models for type safety
- Enum constraints on goal types
- Progress bounds (0-100%)
- Required field validation

## Future Enhancements

### Planned Features
1. Persistent storage (database integration)
2. Multi-agent collaboration
3. Real-time deadline notifications
4. Integration with arts opportunity databases
5. Advanced evaluation metrics
6. Batch goal processing
7. Historical analytics

### Potential Integrations
- Calendar systems (deadline tracking)
- Email notifications
- Document generation (proposals, applications)
- Portfolio management systems
- Grant database APIs
- Conference/exhibition platforms

## Testing Strategy

### Unit Tests
- Model validation (`tests/test_models.py`)
- Utility functions (`tests/test_opik_integration.py`)
- Isolated component testing

### Integration Tests
- Full workflow examples
- Three goal types demonstrated
- End-to-end validation

### Manual Testing
- Demo script (`demo.py`)
- Example workflows (`examples/`)
- Documentation validation

## Deployment Considerations

### Requirements
- Python 3.8+
- OpenAI API access
- (Optional) Opik account
- Environment configuration

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
```

### Running
```bash
# Demo (no API keys needed)
python demo.py

# Full examples (requires OpenAI API key)
python -m examples.speaking_opportunity
python -m examples.exhibition
python -m examples.grant
```

## Conclusion

CuratAI demonstrates a clean, extensible architecture for agentic AI in the arts domain. The system successfully implements autonomous reasoning, action, and adaptation while maintaining observability through Opik integration. The modular design allows for easy extension and customization to meet diverse artist and strategist needs.
