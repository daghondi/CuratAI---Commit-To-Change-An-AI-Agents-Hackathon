"""
Example demonstrating CuratAI helping an artist secure a grant
"""
import uuid
from datetime import datetime, timedelta

from curatai.models import Goal, GoalType, ArtistProfile
from curatai.agents import CuratAIAgent


def main():
    print("=" * 80)
    print("CuratAI Example: Securing a Grant")
    print("=" * 80)
    print()
    
    # Create an artist profile
    artist = ArtistProfile(
        name="Sofia Martinez",
        discipline="Community-Engaged Art",
        expertise_areas=["Social practice", "Community workshops", "Public art"],
        past_achievements=[
            "Community mural project in downtown district",
            "Arts education program for underserved youth",
            "Recipient of Local Arts Council Award"
        ],
        bio="Sofia Martinez creates participatory art projects that strengthen community bonds and cultural identity."
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
        goal_type=GoalType.GRANT,
        title="Secure National Arts Foundation Grant",
        description="Apply for $50,000 grant to fund community art project 'Voices of the Neighborhood'",
        target_date=datetime.now() + timedelta(days=60)
    )
    
    agent.add_goal(goal)
    print(f"Goal Created: {goal.title}")
    print(f"  Type: {goal.goal_type.value}")
    print()
    
    # Reasoning
    print("-" * 80)
    print("AUTONOMOUS REASONING")
    print("-" * 80)
    
    reasoning_result = agent.reason(
        goal,
        context="Grant application deadline is in 60 days. Requires detailed project plan and budget."
    )
    
    if reasoning_result["status"] == "success":
        print("✓ Strategic plan developed")
    print()
    
    # Acting
    print("-" * 80)
    print("TAKING ACTION")
    print("-" * 80)
    
    action_result = agent.act(goal, "Research requirements and prepare proposal")
    
    if action_result["status"] == "success":
        print(f"✓ Progress: {action_result['new_progress']}%")
    print()
    
    print("=" * 80)
    print(f"Final Status: {goal.status.value} | Progress: {goal.progress}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
