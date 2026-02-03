"""
Base Agent with autonomous reasoning, action, and adaptation capabilities
"""
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

from curatai.models import Goal, GoalType, GoalStatus, ArtistProfile, Obstacle
from curatai.utils import opik_tracker

load_dotenv()


class CuratAIAgent:
    """
    Agentic AI that autonomously reasons, acts, and adapts to help artists
    and cultural strategists achieve their professional goals.
    """
    
    # Configuration constants
    DEFAULT_ACTIONS_PER_STEP = 2  # Number of actions to take per step
    PROGRESS_INCREMENT = 20  # Progress percentage increase per action step
    
    def __init__(self, artist_profile: ArtistProfile):
        self.artist_profile = artist_profile
        self.goals: List[Goal] = []
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "gpt-4")
        
    def reason(self, goal: Goal, context: str = "") -> Dict[str, Any]:
        """
        Autonomous reasoning about how to achieve a goal
        Returns a reasoning result with recommended actions
        """
        # Build context for reasoning
        prompt = self._build_reasoning_prompt(goal, context)
        
        # Track reasoning with Opik
        trace = opik_tracker.start_trace(f"reasoning_for_{goal.goal_id}")
        
        try:
            # Use LLM for autonomous reasoning
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            reasoning_output = response.choices[0].message.content
            
            result = {
                "goal_id": goal.goal_id,
                "reasoning": reasoning_output,
                "status": "success"
            }
            
            # Track with Opik
            opik_tracker.track_agent_action(
                action_name="reasoning",
                goal_id=goal.goal_id,
                input_data={"goal": goal.title, "context": context},
                output_data=result,
                metadata={"goal_type": goal.goal_type.value}
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "goal_id": goal.goal_id,
                "error": str(e),
                "status": "error"
            }
            
            opik_tracker.track_agent_action(
                action_name="reasoning_error",
                goal_id=goal.goal_id,
                input_data={"goal": goal.title},
                output_data=error_result,
                metadata={"error_type": type(e).__name__}
            )
            
            return error_result
    
    def act(self, goal: Goal, action_plan: str) -> Dict[str, Any]:
        """
        Execute actions based on reasoning
        Simulates taking concrete steps toward goal achievement
        """
        trace = opik_tracker.start_trace(f"acting_for_{goal.goal_id}")
        
        # Generate specific actions based on goal type
        actions = self._generate_actions(goal, action_plan)
        
        # Record actions
        for action in actions:
            goal.add_action(action)
        
        # Update progress
        if goal.status == GoalStatus.PLANNING:
            goal.status = GoalStatus.IN_PROGRESS
        
        # Increment progress
        goal.progress = min(goal.progress + self.PROGRESS_INCREMENT, 100)
        
        result = {
            "goal_id": goal.goal_id,
            "actions_taken": actions,
            "new_progress": goal.progress,
            "new_status": goal.status.value,
            "status": "success"
        }
        
        # Track with Opik
        opik_tracker.track_agent_action(
            action_name="acting",
            goal_id=goal.goal_id,
            input_data={"action_plan": action_plan},
            output_data=result,
            metadata={"goal_type": goal.goal_type.value}
        )
        
        return result
    
    def adapt(self, goal: Goal, obstacle: Obstacle) -> Dict[str, Any]:
        """
        Adapt to obstacles by generating alternative strategies
        Demonstrates autonomous adaptation capability
        """
        trace = opik_tracker.start_trace(f"adapting_for_{goal.goal_id}")
        
        # Generate adaptation strategy using LLM
        prompt = self._build_adaptation_prompt(goal, obstacle)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            adaptation_strategy = response.choices[0].message.content
            
            # Find the obstacle and mark it as resolved
            for i, obs in enumerate(goal.obstacles):
                if obs.description == obstacle.description and not obs.resolved:
                    goal.resolve_obstacle(i, adaptation_strategy)
                    break
            
            result = {
                "goal_id": goal.goal_id,
                "obstacle": obstacle.description,
                "adaptation_strategy": adaptation_strategy,
                "status": "success"
            }
            
            # Track with Opik
            opik_tracker.track_agent_action(
                action_name="adapting",
                goal_id=goal.goal_id,
                input_data={"obstacle": obstacle.description},
                output_data=result,
                metadata={"goal_type": goal.goal_type.value}
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "goal_id": goal.goal_id,
                "obstacle": obstacle.description,
                "error": str(e),
                "status": "error"
            }
            
            opik_tracker.track_agent_action(
                action_name="adapting_error",
                goal_id=goal.goal_id,
                input_data={"obstacle": obstacle.description},
                output_data=error_result,
                metadata={"error_type": type(e).__name__}
            )
            
            return error_result
    
    def add_goal(self, goal: Goal):
        """Add a new goal for the agent to work on"""
        self.goals.append(goal)
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Retrieve a goal by ID"""
        for goal in self.goals:
            if goal.goal_id == goal_id:
                return goal
        return None
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt that defines agent behavior"""
        return f"""You are CuratAI, an advanced AI agent designed to help artists and cultural strategists 
achieve their professional goals. You have deep knowledge of the arts ecosystem, including:
- Speaking opportunities at conferences, panels, and workshops
- Exhibition opportunities at galleries, museums, and art spaces
- Grant opportunities from foundations, government agencies, and arts organizations

You are working with: {self.artist_profile.to_context_string()}

Your capabilities include:
1. Autonomous Reasoning: Analyze situations and develop strategic plans
2. Action: Generate specific, actionable steps
3. Adaptation: Overcome obstacles with creative solutions

Always provide practical, actionable advice tailored to the artist's profile."""
    
    def _build_reasoning_prompt(self, goal: Goal, context: str) -> str:
        """Build a prompt for reasoning about a goal"""
        prompt = f"""Goal: {goal.title}
Type: {goal.goal_type.value}
Description: {goal.description}
Current Status: {goal.status.value}
Current Progress: {goal.progress}%

"""
        if context:
            prompt += f"Additional Context: {context}\n\n"
        
        if goal.actions_taken:
            prompt += "Actions already taken:\n"
            for action in goal.actions_taken:
                prompt += f"- {action}\n"
            prompt += "\n"
        
        if goal.obstacles:
            prompt += "Obstacles encountered:\n"
            for obs in goal.obstacles:
                status = "Resolved" if obs.resolved else "Active"
                prompt += f"- [{status}] {obs.description}\n"
            prompt += "\n"
        
        prompt += """Please analyze this goal and provide:
1. Strategic reasoning about the best approach
2. Specific next steps to take
3. Potential challenges to anticipate
4. Success metrics to track

Format your response as a clear action plan."""
        
        return prompt
    
    def _build_adaptation_prompt(self, goal: Goal, obstacle: Obstacle) -> str:
        """Build a prompt for adapting to an obstacle"""
        prompt = f"""Goal: {goal.title}
Type: {goal.goal_type.value}
Current Status: {goal.status.value}

Obstacle Encountered: {obstacle.description}

The artist has encountered this obstacle while pursuing their goal. 
Please provide:
1. Analysis of why this obstacle occurred
2. Alternative strategies to overcome it
3. Specific actions to take
4. How to prevent similar obstacles in the future

Format your response as a clear adaptation strategy."""
        
        return prompt
    
    def _generate_actions(self, goal: Goal, action_plan: str) -> List[str]:
        """Generate concrete actions based on goal type and plan"""
        # This could be enhanced with more sophisticated action generation
        base_actions = []
        
        if goal.goal_type == GoalType.SPEAKING_OPPORTUNITY:
            base_actions = [
                f"Research speaking opportunities in {self.artist_profile.discipline}",
                "Prepare speaker proposal and bio",
                "Identify target conferences and events",
                "Reach out to event organizers"
            ]
        elif goal.goal_type == GoalType.EXHIBITION:
            base_actions = [
                "Compile portfolio of work",
                "Research galleries and exhibition spaces",
                "Prepare exhibition proposal",
                "Contact curators and gallery directors"
            ]
        elif goal.goal_type == GoalType.GRANT:
            base_actions = [
                "Research grant opportunities",
                "Review eligibility requirements",
                "Prepare project proposal",
                "Gather supporting materials",
                "Submit grant application"
            ]
        
        # Return a subset based on current progress
        num_actions = min(self.DEFAULT_ACTIONS_PER_STEP, len(base_actions))
        return base_actions[:num_actions]
