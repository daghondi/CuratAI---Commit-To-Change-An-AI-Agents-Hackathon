"""
Example demonstrating CuratAI helping an artist secure an exhibition
"""
import uuid
from datetime import datetime, timedelta

from curatai.models import Goal, GoalType, ArtistProfile, Obstacle
from curatai.agents import CuratAIAgent


def main():
    print("=" * 80)
    print("CuratAI Example: Securing an Exhibition")
    print("=" * 80)
    print()
    
    # Create an artist profile
    artist = ArtistProfile(
        name="James Chen",
        discipline="Contemporary Sculpture",
        expertise_areas=["Kinetic art", "Sustainable materials", "Public installations"],
        past_achievements=[
            "Group exhibition at Modern Art Museum",
            "Public sculpture commission for City Plaza",
            "Featured in Sculpture Magazine"
        ],
        bio="James Chen creates kinetic sculptures that explore movement and sustainability using recycled materials."
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
        goal_type=GoalType.EXHIBITION,
        title="Solo exhibition at Contemporary Arts Gallery",
        description="Secure a solo exhibition showcasing kinetic sculpture series 'Urban Rhythms'",
        target_date=datetime.now() + timedelta(days=180)
    )
    
    agent.add_goal(goal)
    print(f"Goal Created: {goal.title}")
    print(f"  Type: {goal.goal_type.value}")
    print(f"  Status: {goal.status.value}")
    print()
    
    # Reasoning
    print("-" * 80)
    print("AUTONOMOUS REASONING")
    print("-" * 80)
    
    reasoning_result = agent.reason(
        goal,
        context="Gallery focuses on emerging artists with innovative techniques"
    )
    
    if reasoning_result["status"] == "success":
        print("✓ Strategic analysis completed")
    print()
    
    # Acting
    print("-" * 80)
    print("TAKING ACTION")
    print("-" * 80)
    
    action_result = agent.act(goal, "Prepare portfolio and reach out to curator")
    
    if action_result["status"] == "success":
        print(f"✓ Progress: {action_result['new_progress']}%")
        print(f"Actions: {len(action_result['actions_taken'])} completed")
    print()
    
    # Demonstrate adaptation
    print("-" * 80)
    print("ADAPTING TO OBSTACLE")
    print("-" * 80)
    
    obstacle = goal.add_obstacle(
        "Gallery has no available slots for next 18 months"
    )
    
    adaptation_result = agent.adapt(goal, obstacle)
    
    if adaptation_result["status"] == "success":
        print("✓ Adaptation strategy developed")
    print()
    
    print("=" * 80)
    print(f"Final Status: {goal.status.value} | Progress: {goal.progress}%")
    print("=" * 80)


if __name__ == "__main__":
    main()
