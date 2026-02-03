"""
Tests for Opik integration utilities
"""
from curatai.utils import opik_tracker, OpikTracker


def test_opik_tracker_initialization():
    """Test OpikTracker initialization"""
    tracker = OpikTracker()
    
    # Should initialize without errors even if Opik is not configured
    assert tracker is not None
    print("✓ OpikTracker initialization test passed")


def test_opik_tracker_track_action_without_config():
    """Test tracking an action without Opik configuration"""
    tracker = OpikTracker()
    
    # Should not raise errors even if Opik is not configured
    try:
        tracker.track_agent_action(
            action_name="test_action",
            goal_id="test_goal",
            input_data={"test": "input"},
            output_data={"test": "output"}
        )
        print("✓ OpikTracker track action test passed")
    except Exception as e:
        print(f"✗ OpikTracker track action test failed: {e}")
        raise


def test_opik_tracker_evaluate_action():
    """Test evaluating an action"""
    tracker = OpikTracker()
    
    expected = {"key1": "value1", "key2": "value2"}
    actual = {"key1": "value1", "key3": "value3"}
    
    evaluation = tracker.evaluate_action(
        action_name="test_action",
        expected_output=expected,
        actual_output=actual
    )
    
    assert evaluation is not None
    assert "action" in evaluation or "evaluation" in evaluation
    print("✓ OpikTracker evaluate action test passed")


if __name__ == "__main__":
    test_opik_tracker_initialization()
    test_opik_tracker_track_action_without_config()
    test_opik_tracker_evaluate_action()
    print("\n✅ All Opik integration tests passed!")
