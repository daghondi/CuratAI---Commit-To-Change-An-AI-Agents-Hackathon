"""
Unit tests for Opik integration
"""

import unittest
from src.opik_integration.opik_metrics import OpikConfig, OpikMetricsLogger


class TestOpikConfig(unittest.TestCase):
    """Tests for Opik Configuration"""
    
    def setUp(self):
        self.config = OpikConfig()
    
    def test_config_initialization(self):
        """Test config loads properly"""
        self.assertIsNotNone(self.config.workspace)
        self.assertIsNotNone(self.config.project_name)
    
    def test_metrics_defined(self):
        """Test metrics are defined"""
        self.assertGreater(len(self.config.metrics), 0)
        self.assertIn("acceptance_rate", self.config.metrics)
    
    def test_experiments_defined(self):
        """Test experiments are defined"""
        self.assertGreater(len(self.config.experiments), 0)
        self.assertIn("tone_comparison", self.config.experiments)
    
    def test_get_config_dict(self):
        """Test config dictionary export"""
        config_dict = self.config.get_config_dict()
        self.assertIn("metrics", config_dict)
        self.assertIn("experiments", config_dict)


class TestOpikMetricsLogger(unittest.TestCase):
    """Tests for Opik Metrics Logger"""
    
    def setUp(self):
        self.config = OpikConfig()
        self.logger = OpikMetricsLogger(self.config)
    
    def test_log_metric(self):
        """Test logging a metric"""
        self.logger.log_metric("acceptance_rate", 0.35)
        
        summary = self.logger.get_metrics_summary()
        self.assertEqual(summary["total_logged"], 1)
    
    def test_log_experiment_result(self):
        """Test logging experiment result"""
        self.logger.log_experiment_result(
            "tone_comparison",
            "engaging",
            {"draft_quality": 7.8}
        )
        
        summary = self.logger.get_metrics_summary()
        self.assertGreater(summary["total_logged"], 0)
    
    def test_unknown_metric_warning(self):
        """Test logging unknown metric"""
        # Should not raise error
        self.logger.log_metric("unknown_metric", 1.0)


if __name__ == "__main__":
    unittest.main()
