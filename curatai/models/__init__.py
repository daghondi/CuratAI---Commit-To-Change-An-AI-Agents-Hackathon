"""
Data models for CuratAI goals and opportunities
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class GoalType(str, Enum):
    """Types of professional goals for artists and strategists"""
    SPEAKING_OPPORTUNITY = "speaking_opportunity"
    EXHIBITION = "exhibition"
    GRANT = "grant"


class GoalStatus(str, Enum):
    """Status of goal pursuit"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class Obstacle(BaseModel):
    """Represents an obstacle encountered during goal pursuit"""
    description: str
    detected_at: datetime = Field(default_factory=datetime.now)
    resolved: bool = False
    resolution_strategy: Optional[str] = None


class Goal(BaseModel):
    """Represents a professional goal for an artist or strategist"""
    goal_id: str
    goal_type: GoalType
    title: str
    description: str
    target_date: Optional[datetime] = None
    status: GoalStatus = GoalStatus.PLANNING
    progress: int = Field(default=0, ge=0, le=100)
    obstacles: List[Obstacle] = Field(default_factory=list)
    actions_taken: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_obstacle(self, description: str) -> Obstacle:
        """Add a new obstacle to this goal"""
        obstacle = Obstacle(description=description)
        self.obstacles.append(obstacle)
        if self.status != GoalStatus.BLOCKED:
            self.status = GoalStatus.BLOCKED
        return obstacle
    
    def resolve_obstacle(self, obstacle_index: int, resolution_strategy: str):
        """Mark an obstacle as resolved"""
        if 0 <= obstacle_index < len(self.obstacles):
            self.obstacles[obstacle_index].resolved = True
            self.obstacles[obstacle_index].resolution_strategy = resolution_strategy
            
            # If all obstacles are resolved, move back to in_progress
            if all(obs.resolved for obs in self.obstacles):
                self.status = GoalStatus.IN_PROGRESS
    
    def add_action(self, action: str):
        """Record an action taken for this goal"""
        self.actions_taken.append(action)


class ArtistProfile(BaseModel):
    """Profile of an artist or cultural strategist"""
    name: str
    discipline: str  # e.g., visual arts, performing arts, music, etc.
    expertise_areas: List[str] = Field(default_factory=list)
    past_achievements: List[str] = Field(default_factory=list)
    portfolio_url: Optional[str] = None
    bio: Optional[str] = None
    
    def to_context_string(self) -> str:
        """Convert profile to a context string for AI reasoning"""
        context = f"Artist: {self.name}\n"
        context += f"Discipline: {self.discipline}\n"
        if self.expertise_areas:
            context += f"Expertise: {', '.join(self.expertise_areas)}\n"
        if self.bio:
            context += f"Bio: {self.bio}\n"
        if self.past_achievements:
            context += "Past Achievements:\n"
            for achievement in self.past_achievements:
                context += f"  - {achievement}\n"
        return context
