"""
Example demonstrating CuratAI helping an artist secure a speaking opportunity
"""
import uuid
from datetime import datetime, timedelta

from curatai.models import Goal, GoalType, ArtistProfile, Obstacle
from curatai.agents import CuratAIAgent


def main():
    print("=" * 80)
    print("CuratAI Example: Securing a Speaking Opportunity")
    print("=" * 80)
    print()
    
    # Create an artist profile
    artist = ArtistProfile(
        name="Maya Rodriguez",
        discipline="Digital Art and Technology",
        expertise_areas=["AI-generated art", "Interactive installations", "Digital ethics"],
        past_achievements=[
            "Featured in Digital Arts Magazine 2023",
            "Solo exhibition at TechArt Gallery",
            "Winner of Innovation in Arts Award"
        ],
        bio="Maya Rodriguez is a digital artist exploring the intersection of artificial intelligence and human creativity."
    )
    
    print("Artist Profile:")
    print(artist.to_context_string())
    print()
    
    # Initialize the agent
    print("Initializing CuratAI Agent...")
    agent = CuratAIAgent(artist)
    print("✓ Agent initialized\n")
    
    # Create a goal
    goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.SPEAKING_OPPORTUNITY,
        title="Secure speaking engagement at AI & Arts Conference 2024",
        description="Get invited to speak at a major conference about AI-generated art and its ethical implications",
        target_date=datetime.now() + timedelta(days=90)
    )
    
    agent.add_goal(goal)
    print(f"Goal Created: {goal.title}")
    print(f"  Type: {goal.goal_type.value}")
    print(f"  Status: {goal.status.value}")
    print(f"  Progress: {goal.progress}%")
    print()
    
    # Phase 1: Reasoning
    print("-" * 80)
    print("PHASE 1: AUTONOMOUS REASONING")
    print("-" * 80)
    print("Agent is analyzing the goal and developing a strategy...")
    print()
    
    reasoning_result = agent.reason(
        goal, 
        context="The artist wants to establish credibility as a thought leader in AI art"
    )
    
    if reasoning_result["status"] == "success":
        print("✓ Reasoning completed")
        print("\nAgent's Strategic Analysis:")
        print(reasoning_result["reasoning"])
    else:
        print("✗ Reasoning encountered an error:", reasoning_result.get("error"))
    print()
    
    # Phase 2: Acting
    print("-" * 80)
    print("PHASE 2: TAKING ACTION")
    print("-" * 80)
    print("Agent is executing concrete steps toward the goal...")
    print()
    
    action_result = agent.act(
        goal,
        action_plan="Research conferences, prepare proposal, contact organizers"
    )
    
    if action_result["status"] == "success":
        print("✓ Actions executed")
        print(f"\nNew Status: {action_result['new_status']}")
        print(f"Progress: {action_result['new_progress']}%")
        print("\nActions Taken:")
        for action in action_result["actions_taken"]:
            print(f"  • {action}")
    else:
        print("✗ Action encountered an error:", action_result.get("error"))
    print()
    
    # Simulate an obstacle
    print("-" * 80)
    print("PHASE 3: ADAPTING TO OBSTACLES")
    print("-" * 80)
    print("An obstacle has been encountered...")
    print()
    
    obstacle = goal.add_obstacle(
        "Conference has a highly competitive speaker selection process with 200+ applications"
    )
    
    print(f"Obstacle: {obstacle.description}")
    print(f"Goal Status: {goal.status.value}")
    print("\nAgent is developing an adaptation strategy...")
    print()
    
    adaptation_result = agent.adapt(goal, obstacle)
    
    if adaptation_result["status"] == "success":
        print("✓ Adaptation strategy developed")
        print("\nAdaptation Strategy:")
        print(adaptation_result["adaptation_strategy"])
        print()
        print(f"Obstacle Status: {'Resolved' if obstacle.resolved else 'Active'}")
        print(f"Goal Status: {goal.status.value}")
    else:
        print("✗ Adaptation encountered an error:", adaptation_result.get("error"))
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Goal: {goal.title}")
    print(f"Status: {goal.status.value}")
    print(f"Progress: {goal.progress}%")
    print(f"Actions Taken: {len(goal.actions_taken)}")
    print(f"Obstacles Encountered: {len(goal.obstacles)}")
    print(f"Obstacles Resolved: {sum(1 for obs in goal.obstacles if obs.resolved)}")
    print()
    print("CuratAI has demonstrated:")
    print("  ✓ Autonomous Reasoning - Analyzed the goal and developed strategy")
    print("  ✓ Action - Executed concrete steps toward goal achievement")
    print("  ✓ Adaptation - Overcame obstacles with creative solutions")
    print("  ✓ Opik Integration - Tracked all actions for monitoring and evaluation")
    print()


if __name__ == "__main__":
    main()
