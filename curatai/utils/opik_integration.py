"""
Utility functions for Opik integration
"""
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpikTracker:
    """
    Wrapper for Opik tracking functionality
    Handles orchestration, monitoring, and evaluation
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPIK_API_KEY")
        self.workspace = os.getenv("OPIK_WORKSPACE")
        self.enabled = bool(self.api_key and self.workspace)
        
        if self.enabled:
            try:
                import opik
                self.opik = opik
                # Configure Opik client
                opik.configure(
                    api_key=self.api_key,
                    workspace=self.workspace
                )
            except ImportError:
                print("Warning: Opik not installed. Tracking will be disabled.")
                self.enabled = False
            except Exception as e:
                print(f"Warning: Failed to configure Opik: {e}")
                self.enabled = False
    
    def track_agent_action(
        self, 
        action_name: str, 
        goal_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Track an agent action with Opik"""
        if not self.enabled:
            return
        
        try:
            # Log the action to Opik
            self.opik.track(
                name=action_name,
                input=input_data,
                output=output_data,
                tags=[f"goal:{goal_id}"],
                metadata=metadata or {}
            )
        except Exception as e:
            print(f"Warning: Failed to track action with Opik: {e}")
    
    def start_trace(self, trace_name: str) -> Optional[Any]:
        """Start a new trace for orchestrating multiple actions"""
        if not self.enabled:
            return None
        
        try:
            return self.opik.trace(name=trace_name)
        except Exception as e:
            print(f"Warning: Failed to start Opik trace: {e}")
            return None
    
    def evaluate_action(
        self,
        action_name: str,
        expected_output: Dict[str, Any],
        actual_output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate an action's output quality"""
        if not self.enabled:
            return {"evaluation": "disabled"}
        
        try:
            # Simple evaluation logic
            score = 0.0
            if expected_output and actual_output:
                matching_keys = set(expected_output.keys()) & set(actual_output.keys())
                score = len(matching_keys) / max(len(expected_output), 1)
            
            evaluation = {
                "action": action_name,
                "score": score,
                "expected_keys": list(expected_output.keys()) if expected_output else [],
                "actual_keys": list(actual_output.keys()) if actual_output else []
            }
            
            return evaluation
        except Exception as e:
            print(f"Warning: Failed to evaluate with Opik: {e}")
            return {"evaluation": "error", "error": str(e)}


# Global tracker instance
opik_tracker = OpikTracker()
