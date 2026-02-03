"""
Tests for CuratAI models
"""
import uuid
from datetime import datetime, timedelta

from curatai.models import Goal, GoalType, GoalStatus, ArtistProfile, Obstacle


def test_artist_profile_creation():
    """Test creating an artist profile"""
    artist = ArtistProfile(
        name="Test Artist",
        discipline="Test Discipline",
        expertise_areas=["Area 1", "Area 2"],
        past_achievements=["Achievement 1"]
    )
    
    assert artist.name == "Test Artist"
    assert artist.discipline == "Test Discipline"
    assert len(artist.expertise_areas) == 2
    assert len(artist.past_achievements) == 1
    print("✓ Artist profile creation test passed")


def test_goal_creation():
    """Test creating a goal"""
    goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.SPEAKING_OPPORTUNITY,
        title="Test Speaking Opportunity",
        description="Test description"
    )
    
    assert goal.goal_type == GoalType.SPEAKING_OPPORTUNITY
    assert goal.status == GoalStatus.PLANNING
    assert goal.progress == 0
    assert len(goal.obstacles) == 0
    assert len(goal.actions_taken) == 0
    print("✓ Goal creation test passed")


def test_goal_add_obstacle():
    """Test adding obstacles to a goal"""
    goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.EXHIBITION,
        title="Test Exhibition",
        description="Test description"
    )
    
    obstacle = goal.add_obstacle("Test obstacle")
    
    assert len(goal.obstacles) == 1
    assert goal.obstacles[0].description == "Test obstacle"
    assert goal.obstacles[0].resolved == False
    assert goal.status == GoalStatus.BLOCKED
    print("✓ Goal add obstacle test passed")


def test_goal_resolve_obstacle():
    """Test resolving an obstacle"""
    goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.GRANT,
        title="Test Grant",
        description="Test description",
        status=GoalStatus.IN_PROGRESS
    )
    
    obstacle = goal.add_obstacle("Test obstacle")
    assert goal.status == GoalStatus.BLOCKED
    
    goal.resolve_obstacle(0, "Test resolution strategy")
    
    assert goal.obstacles[0].resolved == True
    assert goal.obstacles[0].resolution_strategy == "Test resolution strategy"
    assert goal.status == GoalStatus.IN_PROGRESS
    print("✓ Goal resolve obstacle test passed")


def test_goal_add_action():
    """Test adding actions to a goal"""
    goal = Goal(
        goal_id=str(uuid.uuid4()),
        goal_type=GoalType.SPEAKING_OPPORTUNITY,
        title="Test Speaking",
        description="Test description"
    )
    
    goal.add_action("Action 1")
    goal.add_action("Action 2")
    
    assert len(goal.actions_taken) == 2
    assert goal.actions_taken[0] == "Action 1"
    assert goal.actions_taken[1] == "Action 2"
    print("✓ Goal add action test passed")


def test_artist_profile_to_context_string():
    """Test converting artist profile to context string"""
    artist = ArtistProfile(
        name="Test Artist",
        discipline="Visual Arts",
        expertise_areas=["Painting", "Sculpture"],
        past_achievements=["Award 1", "Award 2"],
        bio="Test bio"
    )
    
    context = artist.to_context_string()
    
    assert "Test Artist" in context
    assert "Visual Arts" in context
    assert "Painting" in context
    assert "Test bio" in context
    assert "Award 1" in context
    print("✓ Artist profile to context string test passed")


if __name__ == "__main__":
    test_artist_profile_creation()
    test_goal_creation()
    test_goal_add_obstacle()
    test_goal_resolve_obstacle()
    test_goal_add_action()
    test_artist_profile_to_context_string()
    print("\n✅ All model tests passed!")
