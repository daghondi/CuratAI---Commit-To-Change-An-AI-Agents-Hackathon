"""
Simple demo of CuratAI without requiring API keys
Shows the structure and workflow
"""
import uuid
from datetime import datetime, timedelta

from curatai.models import Goal, GoalType, GoalStatus, ArtistProfile


def main():
    print("=" * 80)
    print("CuratAI - AI Agents for Artists and Cultural Strategists")
    print("Demo: System Structure and Workflow")
    print("=" * 80)
    print()
    
    # Create an artist profile
    print("Creating Artist Profile...")
    artist = ArtistProfile(
        name="Alex Johnson",
        discipline="Mixed Media Art",
        expertise_areas=["Installation art", "Video art", "Performance"],
        past_achievements=[
            "Participated in Venice Biennale 2022",
            "Solo show at MoMA PS1",
            "Recipient of Guggenheim Fellowship"
        ],
        bio="Alex Johnson is an interdisciplinary artist exploring themes of identity and technology."
    )
    
    print("\n" + "─" * 80)
    print("ARTIST PROFILE")
    print("─" * 80)
    print(artist.to_context_string())
    
    # Create goals for each type
    goals = []
    
    # Speaking opportunity goal
    speaking_goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.SPEAKING_OPPORTUNITY,
        title="Keynote at Digital Arts Summit 2024",
        description="Secure keynote speaking slot at major digital arts conference",
        target_date=datetime.now() + timedelta(days=120),
        status=GoalStatus.PLANNING
    )
    goals.append(speaking_goal)
    
    # Exhibition goal
    exhibition_goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.EXHIBITION,
        title="Solo exhibition at Whitney Museum",
        description="Present new installation series 'Digital Reflections'",
        target_date=datetime.now() + timedelta(days=365),
        status=GoalStatus.IN_PROGRESS,
        progress=35
    )
    exhibition_goal.add_action("Submitted exhibition proposal")
    exhibition_goal.add_action("Met with curator for initial discussion")
    goals.append(exhibition_goal)
    
    # Grant goal
    grant_goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.GRANT,
        title="NEA Art Works Grant",
        description="$75,000 grant for community art project",
        target_date=datetime.now() + timedelta(days=45),
        status=GoalStatus.IN_PROGRESS,
        progress=60
    )
    grant_goal.add_action("Researched grant requirements")
    grant_goal.add_action("Drafted project proposal")
    grant_goal.add_action("Gathered letters of support")
    
    # Add an obstacle
    obstacle = grant_goal.add_obstacle("Budget documentation incomplete")
    goals.append(grant_goal)
    
    # Display goals
    print("\n" + "─" * 80)
    print("PROFESSIONAL GOALS")
    print("─" * 80)
    
    for i, goal in enumerate(goals, 1):
        print(f"\nGoal #{i}: {goal.title}")
        print(f"  Type: {goal.goal_type.value.replace('_', ' ').title()}")
        print(f"  Status: {goal.status.value.replace('_', ' ').title()}")
        print(f"  Progress: {goal.progress}%")
        
        if goal.target_date:
            days_remaining = (goal.target_date - datetime.now()).days
            print(f"  Target: {goal.target_date.strftime('%Y-%m-%d')} ({days_remaining} days)")
        
        if goal.actions_taken:
            print(f"  Actions taken: {len(goal.actions_taken)}")
            for action in goal.actions_taken:
                print(f"    • {action}")
        
        if goal.obstacles:
            print(f"  Obstacles: {len(goal.obstacles)}")
            for obs in goal.obstacles:
                status = "✓ Resolved" if obs.resolved else "⚠ Active"
                print(f"    [{status}] {obs.description}")
    
    # Show agent capabilities
    print("\n" + "=" * 80)
    print("AGENTIC AI CAPABILITIES")
    print("=" * 80)
    
    print("""
CuratAI provides three core agentic AI capabilities:

1. 🧠 AUTONOMOUS REASONING
   - Analyzes professional goals and current status
   - Develops strategic plans tailored to artist's profile
   - Considers arts ecosystem knowledge (conferences, galleries, grants)
   - Uses LLM-powered reasoning for creative problem-solving

2. 🎯 ACTION
   - Executes concrete steps toward goal achievement
   - Generates specific, actionable tasks
   - Tracks progress and updates goal status
   - Adapts action plans based on goal type

3. 🔄 ADAPTATION
   - Detects and responds to obstacles
   - Generates alternative strategies when blocked
   - Learns from challenges to improve future planning
   - Maintains progress even when facing setbacks

4. 📊 OPIK INTEGRATION
   - Orchestrates multi-step workflows
   - Monitors all agent actions and decisions
   - Evaluates effectiveness of strategies
   - Provides insights for continuous improvement
""")
    
    # Show workflow
    print("=" * 80)
    print("TYPICAL WORKFLOW")
    print("=" * 80)
    
    print("""
┌─────────────────────────────────────────────────────────────────────┐
│ 1. Artist creates profile with expertise and past achievements     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. Define professional goal (speaking, exhibition, or grant)       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. Agent REASONS about best approach using AI                      │
│    - Analyzes goal requirements                                     │
│    - Considers artist's strengths                                   │
│    - Develops strategic plan                                        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. Agent ACTS on the plan                                          │
│    - Generates specific actions                                     │
│    - Executes concrete steps                                        │
│    - Tracks progress                                                │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
                    Obstacle detected?
                           │
                    ┌──────┴──────┐
                    │             │
                   Yes            No
                    │             │
                    ▼             ▼
┌──────────────────────────┐  Continue
│ 5. Agent ADAPTS          │  executing
│    - Analyzes obstacle   │  plan
│    - Develops workaround │
│    - Adjusts strategy    │
└──────────────────────────┘
                    │
                    ▼
            Goal Achieved! 🎉
""")
    
    print("=" * 80)
    print("To see the full system in action with AI reasoning:")
    print("  1. Set up your .env file with OpenAI and Opik API keys")
    print("  2. Run: python -m examples.speaking_opportunity")
    print("  3. Run: python -m examples.exhibition")
    print("  4. Run: python -m examples.grant")
    print("=" * 80)


if __name__ == "__main__":
    main()
