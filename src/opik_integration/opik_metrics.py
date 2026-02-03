"""
Opik configuration and metrics tracking

Initializes Opik for workflow orchestration and experiment tracking
"""

import yaml
from typing import Optional

# Opik Configuration (YAML format)
OPIK_CONFIG = """
opik:
  # Opik API configuration
  api_key: "${OPIK_API_KEY}"
  workspace: "curatai-workspace"
  project_name: "curataI-core"
  
  # Logging settings
  logging:
    level: "INFO"
    log_llm_calls: true
    log_agent_calls: true
    
  # Experiment tracking
  experiments:
    enabled: true
    auto_log_metrics: true
    
  # Dashboard
  dashboard:
    enabled: true
    
  # Cost tracking
  cost_tracking:
    enabled: true
    alert_threshold: 100
    
  # Retention
  retention_days: 90
"""


class OpikMetrics:
    """Tracks metrics for Opik monitoring"""
    
    def __init__(self):
        self.metrics = {
            "scout_recall": 0.0,
            "draft_quality": 0.0,
            "user_review_time": 0,
            "acceptance_rate": 0.0,
            "strategy_improvement": 0.0,
            "token_cost": 0
        }
    
    def update_metric(self, name: str, value: float):
        """Update a metric value"""
        if name in self.metrics:
            self.metrics[name] = value
    
    def get_metrics(self) -> dict:
        """Get all metrics"""
        return self.metrics.copy()
    
    def get_metric(self, name: str) -> Optional[float]:
        """Get a specific metric"""
        return self.metrics.get(name)


# Global metrics instance
opik_metrics = OpikMetrics()
